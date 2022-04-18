package coflowsim.traceproducers;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Vector;

import coflowsim.datastructures.Flow;
import coflowsim.datastructures.Job;

public class BenchmarkTraceProducer extends TraceProducer {

  private int NUM_OUT_LINK;

  private int numJobs;

  private int simMinutes;

  private String pathToBenchmarkTraceFile;

  /**
   * @param pathToCoflowBenchmarkTraceFile
   *          Path to the file containing the trace.
   */
  public BenchmarkTraceProducer(String pathToBenchmarkTraceFile) {
    this.pathToBenchmarkTraceFile = pathToBenchmarkTraceFile;
  }

  /**
   * Read trace from file.
   */
  @Override
  public void prepareTrace() {
    FileInputStream fis = null;
    try {
      fis = new FileInputStream(pathToBenchmarkTraceFile);
    } catch (FileNotFoundException e) {
      System.err.println("Couldn't open " + pathToBenchmarkTraceFile);
      System.exit(1);
    }

    BufferedReader br = new BufferedReader(new InputStreamReader(fis));

    // Read number of links and number of jobs in the trace
    try {
      String line = br.readLine();
      String[] splits = line.split("\\s+");

      NUM_OUT_LINK = Integer.parseInt(splits[0]);
      numJobs = Integer.parseInt(splits[1]);
      simMinutes = Integer.parseInt(splits[2]);
    } catch (IOException e) {
      System.err.println("Missing trace description in " + pathToBenchmarkTraceFile);
      System.exit(1);
    }

    // Read numJobs jobs from the trace file
    for (int j = 0; j < numJobs; j++) {
      try {
        String line = br.readLine();
        String[] splits = line.split("\\s+");
        int lIndex = 0;

        String jobName = "JOB-" + splits[lIndex++];
        Job job = jobs.getOrAddJob(jobName);

        int flowNum = Integer.parseInt(splits[lIndex++]);

        
        for (int mID = 0; mID < flowNum; mID++) {
          // String flowName = "FLOW-" + mID;
          // int flowID = mID;

          double jobArrivalTime = 0;

          Vector<Double> flowBytes = new Vector<Double>();
          for (int minutes = 0; minutes < simMinutes; minutes++){
            flowBytes.add(Double.parseDouble(splits[lIndex++]) * 1024);
          }
          
          Vector<Double> delay = new Vector<Double>();

          for (int link = 0; link < NUM_OUT_LINK; link++){
            delay.add(Double.parseDouble(splits[lIndex++]));
          }

          Flow flow = new Flow(flowBytes, jobArrivalTime, delay);

          job.addFlow(flow);
        }

      } catch (IOException e) {
        System.err.println("Missing job in " + pathToBenchmarkTraceFile + ". " + j + "/"
            + numJobs + " read.");
      }
    }
  }

  /** {@inheritDoc} */
  @Override
  public int getNumOutLink() {
    return NUM_OUT_LINK;
  }
}
