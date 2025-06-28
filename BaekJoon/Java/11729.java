import java.io.*;
import java.util.*;

public class Main {
    static StringBuilder sb = new StringBuilder();
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        StringTokenizer st;

        // 첫 줄에 정수 N
        String[] input = br.readLine().split(" ");
        int N = Integer.parseInt(input[0]);

        sb.append((1L << N) - 1).append('\n');

        hanoi(N, 1, 2, 3);
        System.out.print(sb);


        // bw.write(result + "\n");


        bw.flush();
        bw.close();
        br.close();
    }

    public static void hanoi(int n, int start, int temp, int end) {
        if (n == 1) {
            sb.append(start).append(" ").append(end).append('\n');
            return;
        }
        
        hanoi(n-1, start, end, temp);

        sb.append(start).append(" ").append(end).append("\n");

        hanoi(n - 1, temp, start, end);
    }
}
