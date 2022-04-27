package coflowsim.simulators;

import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
// import java.util.Comparator;
// import java.util.HashMap;
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

    if(sharingAlgo == SHARING_ALGO.FAIR || sharingAlgo == SHARING_ALGO.PJF){
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
      if(sharingAlgo == SHARING_ALGO.FIFO || sharingAlgo == SHARING_ALGO.PJF || 
      sharingAlgo == SHARING_ALGO.SCF || sharingAlgo == SHARING_ALGO.DARK){
        order_sort();
      }
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
        jobReduceOrder = 1;
  
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


  private void order_sort(){
    flowsInRacks.clear();
    for(Job j:jobs){
      for(Flow f:j.activeFlows){
        flowsInRacks.add(f);
      }
    }
    if(sharingAlgo == SHARING_ALGO.FIFO){
      Collections.shuffle(flowsInRacks);
    }
    else if(sharingAlgo == SHARING_ALGO.PJF){
      Collections.sort(flowsInRacks, PJFComparator);
    }
    else if(sharingAlgo == SHARING_ALGO.SCF){
      Collections.sort(flowsInRacks, SJFComparator);
    }
    else if(sharingAlgo == SHARING_ALGO.DARK){
      Collections.shuffle(flowsInRacks);
      Collections.sort(flowsInRacks, DARKComparator);
    }
    // for(Flow f : flowsInRacks){
    //   System.out.println(f.learned_pri + " " + f.pri);
    // }
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
    double bytesPerFlow = Constants.RACK_BYTES_PER_SEC / 1000;
    double bytesReduced = 0;
    for(int time_offset = 1; time_offset <= Constants.SIMULATION_QUANTA; time_offset++){
      jobReduceOrder = 0;
      double bytesRemain = bytesPerFlow; 
      Vector<Flow> reduceVec = new Vector<Flow>();
      Vector<Flow> reduceVec1 = new Vector<Flow>();
      double reducePri = 0;
      int flow_index = 0;
      while(flow_index < flowsInRacks.size()){
        Flow f = flowsInRacks.elementAt(flow_index);
        while(f.learned_pri <= reducePri){
          reduceVec.add(f);
          flow_index ++;
          if(flow_index >= flowsInRacks.size()){
            break;
          }
          f = flowsInRacks.elementAt(flow_index);
        }
        reducePri = f.learned_pri;
        if(!reduceVec.isEmpty()){
          while(!reduceVec.isEmpty() && (bytesRemain >= 500)){
            for(Flow ff : reduceVec){
              if(ff.needReduce(curTime + time_offset)){
                bytesReduced = ff.reduce(curTime + time_offset, Math.min(bytesRemain, ff.quantums), jobReduceOrder);
                bytesRemain -= bytesReduced;
                jobReduceOrder += bytesReduced / 500;
              }
              if(!ff.needReduce(curTime + time_offset)){
                reduceVec1.add(ff);
              }
            }
            for(Flow ff : reduceVec1){
              reduceVec.remove(ff);
            }
            reduceVec1.clear();
          }
        }
      }
      
      jobs.manage_buffer(curTime + time_offset);
    }
  }

  private static Comparator<Flow> PJFComparator = new Comparator<Flow>() {
    public int compare(Flow o1, Flow o2) {
      if (o1.pri == o2.pri) return 0;
      return o1.pri < o2.pri? -1 : 1;
    }
  };

  private static Comparator<Flow> SJFComparator = new Comparator<Flow>() {
    public int compare(Flow o1, Flow o2) {
      if (o1.packets.firstElement().arriveTime < o2.packets.firstElement().arriveTime){ return -1;}
      else if(o1.packets.firstElement().arriveTime > o2.packets.firstElement().arriveTime) { return 1;}
      return o1.packets.firstElement().numPackets < o2.packets.firstElement().numPackets? -1 : 1;
    }
  };

  private static Comparator<Flow> DARKComparator = new Comparator<Flow>() {
    public int compare(Flow o1, Flow o2) {
      if (o1.learned_pri == o2.learned_pri) return 0;
      return o1.learned_pri < o2.learned_pri? -1 : 1;
    }
  };
}
