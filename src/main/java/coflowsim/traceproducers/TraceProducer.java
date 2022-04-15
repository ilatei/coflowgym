package coflowsim.traceproducers;

import coflowsim.datastructures.JobCollection;

/**
 * Abstract class for different trace producers.
 */
public abstract class TraceProducer {

  /**
   * {@link JobCollection} object that holds all jobs generated or read by a TraceProducer.
   */
  public final JobCollection jobs;

  /**
   * Constructor for TraceProducer.
   */
  public TraceProducer() {
    jobs = new JobCollection();
  }

  /**
   * Either generates the trace or reads from somewhere.
   */
  public abstract void prepareTrace();

  /**
   * Return the number of out line in the trace.
   * 
   * @return the number of out link.
   */
  public abstract int getNumOutLink();
}
