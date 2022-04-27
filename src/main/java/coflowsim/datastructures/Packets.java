package coflowsim.datastructures;

public class Packets implements Comparable<Packets>{
    public long arriveTime;
    public int numPackets;
    public int bytesPerPacket;
    public long reducedTime;
    public int reducedOrder;
    public boolean dropped = false;
    public int flowId;

    public Packets(long arriveTime, int numPackets){
        this.arriveTime = arriveTime;
        this.numPackets = numPackets;
        this.bytesPerPacket = 500;
    }

    public Packets(long arriveTime, int numPackets, int bytesPerPacket){
        this.arriveTime = arriveTime;
        this.numPackets = numPackets;
        this.bytesPerPacket = bytesPerPacket;
    }

    @Override
    public int compareTo(Packets o) {
        return (int)(arriveTime - o.arriveTime);
    }

    public void setReducedTime(long reducedTime) {
        this.reducedTime = reducedTime;
    }

    public void setReducedOrder(int reducedOrder) {
        this.reducedOrder = reducedOrder;
    }
}
