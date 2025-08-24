import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.*;

public class Main {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int N = Integer.parseInt(br.readLine());

        Queue<Integer> queue = new LinkedList<>();

        for (int i = 0; i < N; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            String command = st.nextToken();

            if (st.hasMoreTokens()) {
                int command2  = Integer.parseInt(st.nextToken());
                queue.add(command2);
            } else {
                switch (command) {
                    case "pop":
                        if (queue.isEmpty()) {
                            System.out.println(-1);
                        } else {
                            System.out.println(queue.poll());
                        }
                        break;
                    case "size":
                        System.out.println(queue.size());
                        break;
                    case "empty":
                        System.out.println(queue.isEmpty() ? 1 : 0);
                        break;
                    case "front":
                        if (queue.isEmpty()) {
                            System.out.println(-1);
                        } else {
                            System.out.println(queue.peek());
                        }
                        break;
                    case "back":
                        if (queue.isEmpty()) {
                            System.out.println(-1);
                        } else {
                            System.out.println(((LinkedList<Integer>) queue).getLast());
                        }
                        break;
                }
            }
        }
    }
}
