package coflowsim.datastructures;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Random;
import java.util.Vector;
// import java.lang.Math;

public class Distribution{
    String pathToDistributionFile = "C:\\Users\\ilatei\\Desktop\\coflowgym\\data\\distribution.txt";
    private Vector<Integer> dis_y = new Vector<Integer>();
    private Vector<Double> dis_x = new Vector<Double>();
    private double base_num;
    private int dis_len;
    private Random r = new Random(20220425);
    public Distribution() throws IOException{
        this.initialize();
    }


    private void initialize() throws IOException{
        FileInputStream fis = null;
        try {
            fis = new FileInputStream(pathToDistributionFile);
        } catch (FileNotFoundException e) {
            System.err.println("Couldn't open " + pathToDistributionFile);
            System.exit(1);
        }

        BufferedReader br = new BufferedReader(new InputStreamReader(fis));
        
        try {
            String line = br.readLine();
            String[] splits = line.split("\\s+");
            this.base_num = Double.parseDouble(splits[0]);
            this.dis_len = Integer.parseInt(splits[1]);

            line = br.readLine();
            splits = line.split("\\s+");
            for(int i = 0; i < dis_len; i++){
                this.dis_y.add(Integer.parseInt(splits[i]));
            }

            line = br.readLine();
            splits = line.split("\\s+");
            for(int i = 0; i < dis_len; i++){
                this.dis_x.add(Double.parseDouble(splits[i]));
            }
            

          } catch (IOException e) {
            System.err.println("Missing trace description in " + pathToDistributionFile);
            System.exit(1);
          }
    }

    public Vector<Integer> getSample(double packetsToFill, int slots){
        Vector<Integer> res = new Vector<Integer>();
        Vector<Integer> ret = new Vector<Integer>();
        int index;
        int ssum = 0;
        int this_fill = 0;
        for(int i=0; i<slots; i++){
            // double randNum = Math.random();
            double randNum = r.nextFloat();
            int l = 0, r = this.dis_len - 1;
            int mid;
            while(l < r){
                mid = (l + r) / 2;
                if(dis_x.get(mid) >= randNum){
                    r = mid;
                }
                else{
                    l = mid + 1;
                }
            }
            index = l;
            // for(index = 0; index < this.dis_len; index++){
            //     if(this.dis_x.get(index) >= randNum){
            //         break;
            //     }
            // }
            if(index == 0){
                this_fill = dis_y.get(index);
            }
            else{
                this_fill = dis_y.get(index-1) + (int)((dis_x.get(index) - randNum) * dis_y.get(index));
            }
            res.add(this_fill);
            ssum += this_fill;
        }
        double ratio = packetsToFill / (double)ssum;
        for(int num : res){
            num = (int)(num * ratio);
            ret.add(num);
        }
        return ret;
    }
}