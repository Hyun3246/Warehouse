import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());
        Stack<Integer> stack = new Stack<>();

        for (int i = 0; i < n; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            String command = st.nextToken();

            if (st.hasMoreTokens()) {
                int value = Integer.parseInt(st.nextToken());
                stack.push(value);
            } else {
                switch (command) {
                    case "pop":
                        if (stack.isEmpty()) {
                            System.out.println(-1);
                        } else {
                            System.out.println(stack.pop());
                        }
                        break;
                    case "size":
                        System.out.println(stack.size());
                        break;
                    case "empty":
                        System.out.println(stack.isEmpty() ? 1 : 0);
                        break;
                    case "top":
                        if (stack.isEmpty()) {
                            System.out.println(-1);
                        } else {
                            System.out.println(stack.peek());
                        }
                        break;
                }
            }
        }
    }
}
