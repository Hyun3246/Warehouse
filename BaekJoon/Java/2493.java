import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.Stack;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        int N = Integer.parseInt(br.readLine());
        int[] towers = new int[N + 1]; // 탑들의 높이 (인덱스는 1부터 사용)
        
        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= N; i++) {
            towers[i] = Integer.parseInt(st.nextToken());
        }

        // --- 여기에 로직 구현 ---
        // 스택을 활용하여 각 탑의 신호를 수신하는 탑을 찾는 로직
        // 결과를 저장할 배열이나 StringBuilder가 필요할 거야.

        Stack<Integer> stack = new Stack<>();

        Integer[] result = new Integer[N + 1];

        StringBuilder sb = new StringBuilder();

        for (int i = N; i > 0; i--) {
            if (stack.isEmpty()) {
                stack.push(i);
            } else {
                while (!stack.isEmpty() && towers[stack.peek()] < towers[i]) {
                    result[stack.pop()] = i;
                }
                stack.push(i);
            }
        }

        for (int i = 1; i <= N; i++) {
            if (result[i] == null) {
                sb.append(0).append(" ");
            } else {
                sb.append(result[i]).append(" ");
            }
        }
        
        // 최종 결과 출력
        System.out.println(sb);
    }
}
