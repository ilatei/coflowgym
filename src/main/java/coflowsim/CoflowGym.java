package coflowsim;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import com.alibaba.fastjson.JSONObject;

import coflowsim.datastructures.Flow;
import coflowsim.datastructures.Job;
import coflowsim.simulators.FlowSimulator;
import coflowsim.simulators.Simulator;
import coflowsim.traceproducers.BenchmarkTraceProducer;
import coflowsim.traceproducers.TraceProducer;
import coflowsim.utils.Constants;
import coflowsim.utils.Constants.SHARING_ALGO;

public class CoflowGym {
    public Simulator simulator;
    private String[] input;

    public static int MAX_COFLOW = 10;

    public CoflowGym(String[] args) {
        input = args;
        // this.initializeSimulator();
        // assert this.simulator.getClass().equals(CoflowSimulatorDark.class);
    }

    /**
     * format "|=|=|" is 
     * activeJobs -> epoch scheduling -> activeJobs -> epoch scheduling 
     * @return
     *      return the observation
     */
    public JSONObject toOneStep(double[] thresholds) {
        // System.out.println("thresholds: "+Arrays.toString(thresholds));
        JSONObject res = new JSONObject();
        JSONObject obs;
        int TIMESATMP = Constants.SIMULATION_SECOND_MILLIS;
        boolean done;
        String completed;
        this.takeAction(thresholds);
        completed = this.simulator.step(TIMESATMP);
        obs = this.simulator.getObservation(TIMESATMP);
        done = this.simulator.prepareActiveJobs(TIMESATMP);
        res.put("observation", obs);
        res.put("completed", completed);
        res.put("MLFQ",this.simulator.getMLFQInfo());
        res.put("done", done);
        return res;
    }

    public JSONObject reset() {
        JSONObject obs;
        int TIMESATMP = 10 * Constants.SIMULATION_SECOND_MILLIS;
        this.initializeSimulator();
        this.simulator.prepareActiveJobs(TIMESATMP);
        obs = this.simulator.getObservation(TIMESATMP);
        return obs;
    }

    /**
     * return info of scheduling in Benchmark
     * @return
     *      return the sum of every job duration in Benchmark
     */
    public String printStats() {
        return this.simulator.printStats(true);
        // System.out.println(this.simulator instanceof CoflowSimulatorDark);
    }

    /**
    return complete information of every coflow.
     */
    public String getCoflowInfo() {
        return this.simulator.getCoflowInfo();
    }

    public void takeAction(double[] thresholds) {
        this.simulator.setPri(thresholds);
    }

    public void initializeSimulator() {
        String[] args = this.input;       
        int curArg = 0;
    
        SHARING_ALGO sharingAlgo = SHARING_ALGO.FAIR;
        if (args.length > curArg) {
          String UPPER_ARG = args[curArg++].toUpperCase();
        //   System.out.println("sharingAlgo(argument): "+UPPER_ARG);
    
          if (UPPER_ARG.contains("FAIR")) {
            sharingAlgo = SHARING_ALGO.FAIR;
          } else if (UPPER_ARG.contains("PJF")) {
            sharingAlgo = SHARING_ALGO.PJF;
          }else if (UPPER_ARG.contains("PFP")) {
            sharingAlgo = SHARING_ALGO.PFP;
          } else if (UPPER_ARG.contains("FIFO")) {
            sharingAlgo = SHARING_ALGO.FIFO;
          } else if (UPPER_ARG.contains("SCF") || UPPER_ARG.contains("SJF")) {
            sharingAlgo = SHARING_ALGO.SCF;
          } else if (UPPER_ARG.contains("NCF") || UPPER_ARG.contains("NJF")) {
            sharingAlgo = SHARING_ALGO.NCF;
          } else if (UPPER_ARG.contains("LCF") || UPPER_ARG.contains("LJF")) {
            sharingAlgo = SHARING_ALGO.LCF;
          } else if (UPPER_ARG.contains("SEBF")) {
            sharingAlgo = SHARING_ALGO.SEBF;
          } else if (UPPER_ARG.contains("DARK")) {
            sharingAlgo = SHARING_ALGO.DARK;
          } else {
            System.err.println("Unsupported or Wrong Sharing Algorithm");
            System.exit(1);
          }
        }
        
        String pathToCoflowBenchmarkTraceFile = args[curArg];

        boolean isOffline = false;
        // int simulationTimestep = Constants.SIMULATION_SECOND_MILLIS;
        // if (isOffline) {
        //   simulationTimestep = Constants.SIMULATION_ENDTIME_MILLIS;
        // }
    
        boolean considerDeadline = false;
        double deadlineMultRandomFactor = 1;
    
        // Create TraceProducer
        TraceProducer traceProducer  = new BenchmarkTraceProducer(pathToCoflowBenchmarkTraceFile); 
        traceProducer.prepareTrace();
    
        // sharingAlgo = SHARING_ALGO.DARK;
        Simulator nlpl = null;
        nlpl = new FlowSimulator(sharingAlgo, traceProducer, isOffline, considerDeadline,
              deadlineMultRandomFactor);
        this.simulator = nlpl;
        
        if(sharingAlgo == SHARING_ALGO.PJF || sharingAlgo == SHARING_ALGO.DARK){
          int[] priority = {2,0,1};
          int index = 0;
          for(Job j : simulator.jobs){
            for(Flow f : j.waitingFlows){
              f.pri = priority[index++];
            }
          }
        }
        // System.out.println("Simulator Class: "+nlpl.getClass().getName());
    }

    public static void main(String[] args) throws IOException {
        String outpath = "C:\\Users\\ilatei\\Desktop\\coflowgym\\data\\pjf_result.txt";
        File file = new File(outpath);
        FileWriter writer = new FileWriter(file);

        String[] args1 = {"DARK", "C:\\Users\\ilatei\\Desktop\\coflowgym\\scripts\\test0.txt"};
        CoflowGym gym = new CoflowGym(args1);
        // double initVal = 10485760.0;
        double[] thresholds = {2,2,1};
        // thresholds[0] = initVal;
        // for (int i = 0; i < 3; ++i) {
        //     thresholds[i] = Math.random();
        // }
        System.out.println("start");
        for (int k = 0; k < 1; ++k) {
            gym.reset();
            for (int i = 0; i < 3600 * 10; ++i) {
                JSONObject res = gym.toOneStep(thresholds);
                // System.out.println("Step: \n"+ res.get("observation"));
                JSONObject js = (JSONObject)(res.get("observation"));
                // System.out.println(js);
                writer.write(js.toJSONString() + "\n");
                gym.takeAction(thresholds);
                if (res.get("done").equals(true)) break;
            }
            // System.out.println("\nResult: ");
            // gym.printStats();
        }
        writer.close();
    }
}