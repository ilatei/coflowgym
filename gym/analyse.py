import numpy as np 
import matplotlib.pyplot as plt
import codecs
import sys, math
from benchdata import exp4_benchmark_data
from util import toFactor

def stats_action(file):
    with open(file, 'r') as f:
        actions = []

        line = f.readline()
        while line:
            pos = line.find("env_action")
            if pos != -1:
                action = eval(line[:pos].split(":")[-1])
                actions.append(action)

            line = f.readline()
        # print(actions[:10])
    actions = np.array(actions)
    N = len(actions[0])
    plt.figure()
    n = math.ceil(math.sqrt(N))
    for i in range(N):
        plt.subplot("%s%s%s"%(n, n, i+1))
        cdf = toCDF(actions[:, i])
        plt.plot(cdf[:, 0], cdf[:, 1])
        plt.xlabel("action[%s]"%i)

def toCDF(data_l):
    """ 
    data is discrete.
    example:
    [1,1,2,3] -> [[1, 0.5], [2, 0.5], [2, 0.75], [3, 0.75], [3, 1.0]]
    """
    l_dict = {}
    for e in sorted(data_l):
        if e in l_dict:
            l_dict[e] += 1
        else:
            l_dict[e] = 1 
    l_sum = 0 
    res = [[0, 0]] 
    for e in sorted(l_dict):
        l_sum += l_dict[e]
        res.append([e, res[-1][1]])
        res.append([e, l_sum/len(data_l)])
    del res[:2]
    return np.array(res)

def toPercentile(cdf, num=10):
    count = 1
    percentile = []
    for e in cdf:
        while e[1] > count/num:
            percentile.append(e[0])
            count += 1
    return percentile

def benchmark_analyse(benchmark_file):
    with open(benchmark_file, "r") as f:
        time = []
        mappers = []
        reducers = []
        shuffle_t = []

        line = f.readline()
        num_machines, num_jobs = (eval(word) for word in line.split())
        print("Number of machines:", num_machines)
        print("Number of jobs:", num_jobs)
        for i in range(num_jobs):
            line = f.readline()
            words = line.split()
            time.append(eval(words[1]))

            m = eval(words[2])
            r = eval(words[3+m])
            total = 0
            for reduce in words[4+m:]:
                total += eval(reduce.split(":")[-1])
            mappers.append(m)
            reducers.append(r)
            shuffle_t.append(total)
        
        ##
        # print(time)
        # print(mappers)
        # print(reducers)
        shuffle_t = np.array(shuffle_t)
        plt.figure()

        plt.subplot(221)
        plt.plot(shuffle_t)
        plt.xlabel("No")
        plt.ylabel("shuffle size/MB")
        
        plt.subplot(222)
        plt.plot(shuffle_t[:100])
        plt.xlabel("No")
        plt.ylabel("shuffle size/MB")

        plt.subplot(223)
        plt.plot(time, shuffle_t)
        plt.xlabel("arrive time/ms")
        plt.ylabel("shuffle size/MB")

        plt.subplot(224)
        plt.plot([m*r for m,r in zip(mappers, reducers)])
        plt.xlabel("No")
        plt.ylabel("width")

        plt.figure()
        test_sf = shuffle_t[:100]
        test_cdf = np.array(toCDF(test_sf))
        print("100coflows Percentile(MB):", toPercentile(test_cdf, num=7))
        print("Benchmark Percentile(MB):", toPercentile(toCDF(shuffle_t), num=7))
        plt.plot(test_cdf[:,0], test_cdf[:,1])
        plt.xlabel("shuffle size/MB")
        plt.ylabel("probability")

def dark_analyse():
    with open("doc/dark.txt", "r") as f:
        durations = []
        shuffle_t = []

        line = f.readline()
        while line:
            if line.startswith("JOB"):
                words = line.split()
                start_time = eval(words[1])
                finish_time = eval(words[2])
                total_shuffle = eval(words[5])
                duration = eval(words[-3])
                
                durations.append(duration)
                shuffle_t.append(total_shuffle)
                if finish_time - start_time != duration:
                    print(words[0], "time doesn't match!")

            line = f.readline()
        ##
        plt.figure()
        plt.plot(shuffle_t)
        plt.xlabel("JOB")
        plt.ylabel("Shuffle/B")

def parse_log(file):
    """
    Parse log file to get training information.
    @return:
        result: runtime of benchmark in a episode
        ep_reward: total rewards accumulated in a episode
    """
    with open(file, 'r') as f:
        result = []
        ep_reward = []

        line = f.readline()
        while line:
            if line.startswith("result:"):
                res = eval(line.split()[1])
                # print(res)
                result.append(res)

            line = f.readline()
            if line.find("ep_reward") != -1:
                rs = eval(line.split()[-1])
                # print(rs)
                ep_reward.append(rs)
        return result, ep_reward

def plot_compare(result, ep_reward, newfigure=True, is_benchmark=True):
    if newfigure:
        plt.figure()
    x = list(range(len(result)))

    if is_benchmark:
        comp = [2.4247392E7, 4.3473352E7, 1.5005968E7]
    else:
        comp = [326688.0, 612776.0, 281880.0]
    plt.plot(x, result, 'b.-')
    plt.plot(x, [comp[0]]*len(x), "red") # DARK
    plt.plot(x, [comp[1]]*len(x), "cyan") # FIFO
    plt.plot(x, [comp[2]]*len(x), "lawngreen") # SEBF
    plt.legend(["DRL", "DARK", "FIFO", "SEBF"])
    plt.xlabel("episode")
    plt.ylabel("ep_runtime")

    # plt.figure()
    # plt.plot(x, [-r for r in ep_reward])
    # plt.scatter(x, [-r for r in ep_reward])

def validate_reward(result, ep_reward, newfigure=True):
    if newfigure:
        plt.figure()
    plt.scatter(result, ep_reward)
    f = np.poly1d(np.polyfit(result, ep_reward, 1))
    print(f)
    plt.plot(result, f(result), 'y')
    plt.xlabel("ep_runtime")
    plt.ylabel("ep_total_reward")

def analyse_reward(file):
    with open(file, "r") as f:
        rs = []

        line = f.readline()
        while line:
            start = line.find("reward:")
            if start != -1:
                words = line[start:].split()
                r = eval(words[1])
                rs.append(r)
            line = f.readline()
        plt.figure()
        p = rs[:500]
        plt.scatter(range(len(p)), p)

def analyse_mlfq():
    with open("log/mlfq.txt", "r") as f:
        mlfqs = []
        line = f.readline()
        while line:
            if line.startswith("MLFQ"):
                mq = eval(line.split(":")[-1])
                mlfqs.append(mq)
            line = f.readline()
        coflow_mlfq = [sum(mlfq) for mlfq in mlfqs]
        plt.figure("Number in MLFQ")
        plt.subplot(211)
        plt.scatter(range(len(coflow_mlfq)), coflow_mlfq, marker='.')
        plt.ylabel("number of coflow")
        plt.xlabel("step")
        cdf = toCDF(coflow_mlfq)
        plt.subplot(212)
        plt.plot(cdf[:, 0], cdf[:, 1])
        plt.xlabel("number of coflow")
        plt.ylabel("cdf")
    if True:
        with open("log/result.txt") as f:
            mlfqs = []
            line = f.readline()
            while line:
                if line.startswith("MLFQ"):
                    mq = eval(line.split(":")[-1])
                    mlfqs.append(mq)
                line = f.readline()
            count = 0
            for mq in mlfqs:
                if np.sum(np.array(mq) > 1) > 0:
                    count += 1
            print("Length of samples:", len(mlfqs))
            print("count of Coflow in MLFQ is more than 1:", count/len(mlfqs))

def analyse_samples():
    with open("log/sample_1.txt") as f:
        actions = []
        results = []
        
        line = f.readline()
        while line:
            if line.startswith("Action"):
                pos = line.find("result")
                res = eval(line[pos:].split(":")[-1])
                if res < 326688:
                    act = eval(line[:pos].split(":")[-1])
                    actions.append(act)
                    results.append(res)
            line = f.readline()
        # for act, res in zip(actions, results):
        #     print(toFactor(act, 1024), res)
        print("Minimum Result:", min(results))

def analyse_log(exp_no):

    if exp_no == 1:
        res1, ep_r1 = parse_log("doc/log/1_log.txt")
        res2, ep_r2 = parse_log("doc/log/2_log.txt")
        print("Number of samples in log_1", len(res1))
        print("Number of samples in log_2", len(res2))
        result, ep_reward = np.array(res1+res2), np.array(ep_r1+ep_r2)
        validate_reward(result[result < 2.5*1e7], ep_reward[result < 2.5*1e7])
    if exp_no is 2:
        result, ep_reward = parse_log(("doc/log/3_log.txt"))
        plt.subplot(211)
        validate_reward(result, ep_reward, newfigure=False)
        plt.subplot(212)
        plot_compare(result, ep_reward, newfigure=False)
    if exp_no is 3:
        result, ep_reward = parse_log("doc/log/4_log.txt")
        result_2, ep_reward_2 = parse_log("doc/log/5_log.txt")
        plt.subplot(221)
        validate_reward(result, ep_reward, newfigure=False)
        plt.title("alpha=0.6")
        plt.subplot(222)
        validate_reward(result_2, ep_reward_2, newfigure=False)
        plt.title("alpha=1")
        plt.subplot(223)
        plot_compare(result, ep_reward, newfigure=False)
        plt.subplot(224)
        plot_compare(result_2, ep_reward_2, newfigure=False)

        plt.figure()
        res100, ep_r_100 = parse_log("doc/log/1_log_100.txt")
        plt.subplot(221)
        validate_reward(res100, ep_r_100, newfigure=False)
        plt.title("100coflows: alpha=0")
        plt.subplot(223)
        plot_compare(res100, ep_r_100, newfigure=False, is_benchmark=False)

        result_6, ep_reward_6 = parse_log("doc/log/6_log.txt")
        plt.subplot(222)
        validate_reward(result_6, ep_reward_6, newfigure=False)
        plt.title("alpha=0")
        plt.subplot(224)
        plot_compare(result_6, ep_reward_6, newfigure=False)
    if exp_no is 4:
        result100, ep_reward_100 = parse_log("doc/log/2_log_100.txt")
        plt.subplot(221)
        validate_reward(result100, ep_reward_100, newfigure=False)
        plt.title("100coflows")
        plt.subplot(223)
        plot_compare(result100, ep_reward_100, is_benchmark=False, newfigure=False)
        # result, ep_reward = parse_log("doc/log/7_log.txt")
        result, ep_reward = exp4_benchmark_data()
        plt.subplot(222)
        validate_reward(result, ep_reward, newfigure=False)
        plt.subplot(224)
        plot_compare(result, ep_reward, newfigure=False)
    if exp_no is 5:
        res100, ep_r_100 = parse_log("doc/log/3_log_100.txt")
        plt.subplot(221)
        validate_reward(res100, ep_r_100, newfigure=False)
        plt.title("100coflows")
        plt.subplot(223)
        plot_compare(res100, ep_r_100, is_benchmark=False, newfigure=False)
        res, ep_r = parse_log("doc/log/8_log.txt")
        plt.subplot(222)
        validate_reward(res, ep_r, newfigure=False)
        plt.subplot(224)
        plot_compare(res, ep_r, newfigure=False)
    if exp_no is 6:
        res100, ep_r_100 = parse_log("doc/log/4_log_100.txt")
        plt.subplot(211)
        plot_compare(res100, ep_r_100, is_benchmark=False, newfigure=False)
        plt.title("100coflows")
        plt.subplot(212)
        plt.plot(ep_r_100)
        plt.xlabel("episode")
        plt.ylabel("ep_reward")

    ## 
    if exp_no < 0:
        result, ep_reward = parse_log(("log/log.txt"))
        print("Number of samples:", len(result))
        print(len(result))
        # print(ep_reward)
        result, ep_reward = np.array(result), np.array(ep_reward)

        # validate_reward(result[result < 350000], ep_reward[result < 350000])
        plot_compare(result, ep_reward, is_benchmark=False, newfigure=False)
        # plt.figure("Exp")
        # plt.subplot(221)
        # plt.subplot(222)
        # validate_reward(result, ep_reward, newfigure=False)
        # plt.subplot(223)
        # plt.plot(ep_reward)
        # plt.ylabel("ep_reward")
        # plt.xlabel("episode")
        # plt.subplot(224)
        # cdf = toCDF(result)
        # plt.plot(cdf[:, 0], cdf[:, 1])
        # plt.xlabel("runtime")
        # plt.ylabel("CDF")

if __name__ == "__main__":
    
    analyse_log(-6)

    # stats_action("log/log.txt")
    
    analyse_mlfq()

    # benchmark_analyse("scripts/FB2010-1Hr-150-0.txt")

    # dark_analyse()

    analyse_samples()

    plt.show()