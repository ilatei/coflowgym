package coflowsim.simulators;

import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Random;
import java.util.Vector;

import coflowsim.datastructures.Flow;
import coflowsim.datastructures.Job;
import coflowsim.traceproducers.TraceProducer;
import coflowsim.utils.Constants;
import coflowsim.utils.Constants.SHARING_ALGO;

/**
 * Implements {@link coflowsim.simulators.Simulator} for flow-level scheduling policies (FAIR and
 * PFP).
 */
public class FlowSimulator extends Simulator {

  /**
   * {@inheritDoc}
   */
  public FlowSimulator(
      SHARING_ALGO sharingAlgo,
      TraceProducer traceProducer,
      boolean offline,
      boolean considerDeadline,
      double deadlineMultRandomFactor) {

    super(sharingAlgo, traceProducer, offline, considerDeadline, deadlineMultRandomFactor);
    assert (sharingAlgo == SHARING_ALGO.FAIR || sharingAlgo == SHARING_ALGO.PFP);

    if(sharingAlgo == SHARING_ALGO.FAIR || sharingAlgo == SHARING_ALGO.PFP){
      Random random = new Random();
      for (Job j : jobs){
        for(Flow f : j.waitingFlows){
          f.randomLink = random.nextInt(NUM_OUT_LINK);
        }
      }
    }
  }

  /** {@inheritDoc} */
  @Override
  protected void uponJobAdmission(Job j) {
    j.currentTime = CURRENT_TIME;
    Vector<Flow> flow2remove = new Vector<Flow>();
    for (Flow f: j.waitingFlows) {
      if(f.getArriveTime() <= CURRENT_TIME){
        j.onFlowSchedule(f);
        flow2remove.add(f);
      }
      else {
        break;
      }
    }
    for (Flow f : flow2remove){
      j.waitingFlows.remove(f);
    }
  }

  /** {@inheritDoc} */
  @Override
  protected void onSchedule(long curTime) {
    if (sharingAlgo == SHARING_ALGO.FAIR) {
      fairShare(curTime, Constants.SIMULATION_QUANTA);
    } else {
      proceedFlowsInAllRacksInSortedOrder(curTime, Constants.SIMULATION_QUANTA);
    }
  }

  /** {@inheritDoc} */
  @Override
  protected void removeDeadJob(Job j) {
    activeJobs.remove(j.jobName);
  }

  /**
   * Flow-level fair sharing
   * 
   * @param curTime
   *          current time
   * @param quantaSize
   *          size of each simulation time step
   */
  private void fairShare(long curTime, long quantaSize) {
    // Calculate the number of outgoing flows
    jobReduceOrder = 1;
    int[] numLinkFlows = new int[NUM_OUT_LINK];
    double[] bytesPerFlow = new double[NUM_OUT_LINK];
    Arrays.fill(numLinkFlows, 0);
    Arrays.fill(bytesPerFlow, 0);
    for (Job j : jobs){
      for(Flow f : j.activeFlows){
        numLinkFlows[f.randomLink] ++;
      }
    }

    for(int link=0; link < NUM_OUT_LINK; link++){
      bytesPerFlow[link] = Constants.RACK_BYTES_PER_SEC / 1000 / numLinkFlows[link];
    }

    for(int time_offset = 1; time_offset <= Constants.SIMULATION_QUANTA; time_offset++){ 
      for (int i = 0; i < NUM_OUT_LINK; i++) {
        // Vector<Flow> flowsToRemove = new Vector<Flow>();
        // Vector<Flow> flowsToAdd = new Vector<Flow>();
  
        for (Job j : jobs){
          for(Flow f : j.activeFlows){
            if(f.needReduce(curTime + time_offset)){
              f.reduce(curTime + time_offset, bytesPerFlow[f.randomLink], jobReduceOrder++);
            }
  
            if(f.bytesRemaining <= Constants.ZERO){
              j.onFlowFinish(f);
            }
          }
        }
        jobs.manage_buffer(curTime + time_offset);
      }
    }
  }

  /**
   * Proceed flows in each rack in the already-determined order; e.g., shortest-first of PFP or
   * earliest-deadline-first in the deadline-sensitive scenario.
   * 
   * @param curTime
   *          current time
   * @param quantaSize
   *          size of each simulation time step
   */
  private void proceedFlowsInAllRacksInSortedOrder(long curTime, long quantaSize) {
    HashMap<Flow, Job> flow2Job = new HashMap<Flow,Job>();
    Vector<Vector<Flow>> allActiveFlow = new Vector<Vector<Flow>>(NUM_OUT_LINK);
    double[] bytesRemainPerLink = new double[NUM_OUT_LINK];
    Arrays.fill(bytesRemainPerLink, Constants.RACK_BYTES_PER_SEC / 1024 * quantaSize);

    for (Job j : jobs){
      for(Flow f : j.activeFlows){
        flow2Job.put(f, j);
        allActiveFlow.elementAt(f.randomLink).add(f);
      }
    }

    for(Vector<Flow> ff : allActiveFlow){
      ff.sort(new Comparator<Flow>() {
        public int compare(Flow f1, Flow f2){
          return (int)(f1.bytesRemaining - f2.bytesRemaining);
        }
      });
    }

    for(Vector<Flow> ff : allActiveFlow){
      for(Flow f : ff){
        if(bytesRemainPerLink[f.randomLink] <= 0){
          continue;
        }
        double bytesPerFlow = Math.min(f.bytesRemaining, bytesRemainPerLink[f.randomLink]);
        f.bytesRemaining -= bytesPerFlow;
        bytesRemainPerLink[f.randomLink] -= bytesPerFlow;

        if(f.bytesRemaining <= 0){
          flow2Job.get(f).onFlowFinish(f);
        }
      }
    }
  }
}
