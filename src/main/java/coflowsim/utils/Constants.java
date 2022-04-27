package coflowsim.utils;

import coflowsim.simulators.Simulator;

/**
 * Constants used throughout the simulator.
 */
public class Constants {

  /**
   * Scheduling/sharing algorithms supported by the {@link Simulator}
   */
  public enum SHARING_ALGO {
    /**
     * Flow-level fair sharing.
     */
    FAIR,
    PJF,
    /**
     * Per-flow SRTF priority and EDF for deadline-sensitive flows.
     */
    PFP,
    /**
     * First-In-First-Out at the coflow level.
     */
    FIFO,
    /**
     * Order coflows by length.
     */
    SCF,
    /**
     * Order coflows by width.
     */
    NCF,
    /**
     * Order coflows by total size.
     */
    LCF,
    /**
     * Order coflows by skew.
     */
    SEBF,
    /**
     * Use the non-clairvoyant scheduler.
     */
    DARK,
    /**
     * Use coflows by total size in MLFQ
     */
    SSCF,
  }

  /**
   * For floating-point comparisons.
   */
  public static final double ZERO = 1e-3;

  /**
   * Constant for values we are not sure about.
   */
  public static final int VALUE_UNKNOWN = -1;

  /**
   * Constant for values we don't care about.
   */
  public static final int VALUE_IGNORED = -2;

  /**
   * Number of parallel flows initiated by each reducer.
   * Hadoop/Spark default is 5.
   */
  public static final int MAX_CONCURRENT_FLOWS = 5;

  /**
   * Capacity constraint of a rack in bps.
   */
  public static final double RACK_BITS_PER_SEC = 15.0 * 1024 * 1048576;

  /**
   * Capacity constraint of a rack in Bps.
   */
  public static final double RACK_BYTES_PER_SEC = RACK_BITS_PER_SEC / 8.0;

  /**
   * Number of milliseconds in a second of {@link Simulator}.
   * An epoch of {@link Simulator#simulate(int)}.
   */
  public static final int SIMULATION_SECOND_MILLIS = 1000;

  /**
   * Time step of {@link Simulator#simulate(int)}.
   */
  public static final int SIMULATION_QUANTA = 10;

  /**
   * {@link Simulator#simulate(int)} completes after this time.
   */
  public static final int SIMULATION_ENDTIME_MILLIS = 24 * 3600 * SIMULATION_SECOND_MILLIS;

  public static final int BUFFER_PER_FLOW = 100; //packets
}
