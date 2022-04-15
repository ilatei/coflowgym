package coflowsim.datastructures;

import java.util.Vector;
import java.util.concurrent.atomic.AtomicInteger;

import com.alibaba.fastjson.JSONObject;

/**
 * Information about individual flow.
 */
public class Flow implements Comparable<Flow> {
  static AtomicInteger nextId = new AtomicInteger();
  private int id;
  private double arriveTime;
  private double scheduleTime;
  private double finishTime;

  private final double totalBytes = 1000;
  private final int slots = 1000;

  public int randomLink;
  public double bytesRemaining;
  public double currentBps;
  public boolean consideredAlready;
  public Vector<Double> delay;
  public Vector<Double> flowBytes;
  public Vector<Packets> packets;
  public Vector<Packets> reducedPackets;

  /**
   * Constructor for Flow.
   * 
   * @param totalBytes
   *          size in bytes.
   */
  public Flow(Vector<Double> flowBytes, double arriveTime, Vector<Double> delay) {
    this.id = nextId.incrementAndGet();
    this.arriveTime = arriveTime;
    this.flowBytes = flowBytes;
    this.delay = delay;

    this.packets = new Vector<Packets>();
    this.reducedPackets = new Vector<Packets>();

    this.bytesRemaining = totalBytes;
    this.currentBps = 0.0;
    this.consideredAlready = false;
  }

  /**
   * For the Comparable interface.
   */
  public int compareTo(Flow arg0) {
    return id - arg0.id;
  }

  /** {@inheritDoc} */
  @Override
  public String toString() {
    return "FLOW-" + id;
  }

  public boolean fillPackets(long timeNow, int timeSlot){
    double packetsToFill = getbpsByTime(timeNow) / 8  / 500;
    if (packetsToFill < 0){
      return false;
    }

    for(int i=0; i<slots; i++){
      packets.add(new Packets(timeNow + timeSlot / slots * i, (int)packetsToFill/slots));
    }
    return true;
  }

  public double getbpsByTime(long timeNow){
    long timeNowMinute = timeNow / 1000 / 60;
    if (timeNowMinute >= flowBytes.size()){
      return -1;
    }
    else return flowBytes.elementAt((int)timeNowMinute);
  }

  public double getFlowSize() {
    return totalBytes;
  }

  public double getArriveTime() {
    return arriveTime;
  }

  public void setFinishTime(double finishTime) {
      this.finishTime = finishTime;
  }

  public void setScheduleTime(double scheduleTime) {
      this.scheduleTime = scheduleTime;
  }

  public double getWaitingTime(){
    return scheduleTime - arriveTime;
  }

  public double getExcutionTime(){
    return finishTime - scheduleTime;
  }

  public boolean needReduce(long timeNow){
    for(Packets p : packets){
      if(timeNow <= p.arriveTime){
        return false;
      }
      if(p.numPackets > 0){
        return true;
      }
    }
    return false;
  }

  public void reduce(long curTime, double reduceSize, int jobReduceOrder) {
    Vector<Packets> packetsToReduce = new Vector<Packets>();
    int numPacketsToReduce = (int)reduceSize / 500;
    for(Packets p:packets){
      if(p.arriveTime >= curTime || numPacketsToReduce == 0){
        break;
      }
      if(p.numPackets > 0){
        if(numPacketsToReduce >= p.numPackets){
          p.setReducedTime(curTime);
          p.setReducedOrder(jobReduceOrder);
          packetsToReduce.add(p);
          reducedPackets.add(p);
          numPacketsToReduce -= p.numPackets;
        }
        else{
          Packets temp_packet = new Packets(p.arriveTime, numPacketsToReduce);
          temp_packet.setReducedTime(curTime);
          reducedPackets.add(temp_packet);
          p.numPackets -= numPacketsToReduce;
          numPacketsToReduce = 0;
        }
      }
    }
    for(Packets p:packetsToReduce){
      packets.remove(p);
    }
  }

  public JSONObject calResult(){
    int packets_dropped = 0;
    int packets_deliverd = 0;
    int packets_delay = 0;
    for(Packets p : packets){
      packets_dropped += p.numPackets;
    }
    for(Packets p : reducedPackets){
      packets_deliverd += p.numPackets;
      packets_delay += p.numPackets * (p.reducedTime - p.arriveTime);
    }
    // packets.clear();
    reducedPackets.clear();
    JSONObject res = new JSONObject();
    res.put("dropRate", (double)packets_dropped / (packets_dropped + packets_deliverd));
    res.put("delay", (double)packets_delay / packets_deliverd);
    res.put("througthput", (double)packets_deliverd * 500 * 8 / 1024 / 1024);
    return res;
  }
}
