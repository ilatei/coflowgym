package coflowsim.datastructures;
import java.util.Vector;
import coflowsim.utils.Constants;

/**
 * Information about individual Job/Coflow.
 */
public class Job implements Comparable<Job> {

  public final String jobName;
  public final int jobID;

  public double startTime;
  public double currentTime;
  public double finishTime;

  public Vector<Flow> activeFlows;
  public Vector<Flow> waitingFlows;
  public Vector<Flow> finishFlows;

  /**
   * Constructor for Job.
   * 
   * @param jobName
   *          the name of the job.
   * @param jobID
   *          a unique ID of the job.
   */
  public Job(String jobName, int jobID) {
    this.jobName = jobName;
    this.jobID = jobID;

    activeFlows = new Vector<Flow>();
    waitingFlows = new Vector<Flow>();
    finishFlows = new Vector<Flow>();

    resetJobStates();
  }

  /**
   * Adds a task to the job and updates relevant bookkeeping.
   * 
   * @param task
   *          {@link coflowsim.datastructures.Task} to add.
   */
  public void addFlow(Flow flow) {
    waitingFlows.add(flow);
  }

  /**
   * Stuff to do when a task gets scheduled.
   * 
   * @param task
   *          {@link coflowsim.datastructures.Task} under consideration.
   */
  public void onFlowSchedule(Flow flow) {
    flow.setScheduleTime(currentTime);
    activeFlows.add(flow);
  }

  /**
   * Stuff to do when a task completes.
   * 
   * @param task
   *          {@link coflowsim.datastructures.Task} under consideration.
   */
  public void onFlowFinish(Flow flow) {
    flow.setFinishTime(currentTime);
    finishFlows.add(flow);
  }

  /**
   * Coflow completion time as determined by the simulator.
   * 
   * @return coflow completion time or {@link coflowsim.utils.Constants#VALUE_UNKNOWN} on error.
   */
  public double getSimulatedDuration() {
    return finishTime - startTime;
  }

  /**
   * For the Comparable interface.
   */
  public int compareTo(Job arg0) {
    return jobName.compareTo(arg0.jobName);
  }

  private void resetJobStates() {
    startTime = Constants.VALUE_UNKNOWN;
    currentTime = Constants.VALUE_UNKNOWN;
    finishTime = Constants.VALUE_UNKNOWN;
  }

  public void fillJobs(long timeNow, int timeSlot){
    Vector<Flow> flow2remove = new Vector<Flow>(); 
    for(Flow f : activeFlows){
      if(!f.fillPackets(timeNow, timeSlot)){
        flow2remove.add(f);
      }
    }
    for(Flow f : flow2remove){
      activeFlows.remove(f);
    }
  }

  /** {@inheritDoc} */
  @Override
  public String toString() {
    return jobName;
  }
}