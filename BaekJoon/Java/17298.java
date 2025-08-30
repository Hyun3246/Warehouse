import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.Stack;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        int N = Integer.parseInt(br.readLine());
        int[] A = new int[N];
        
        StringTokenizer st = new StringTokenizer(br.readLine(), " ");
        for (int i = 0; i < N; i++) {
            A[i] = Integer.parseInt(st.nextToken());
        }
        
        // 이 배열 A를 바탕으로 오큰수를 찾는 로직을 여기에 구현

        Integer[] result = new Integer[N];

        for (int i = 0; i < N; i++) {
            result[i] = -1;
        }

        Stack<Integer> stack = new Stack<>();       // 아직 오큰수를 찾지 못한 인덱스들

        // 스택에는 값을 직접 넣지 않고, 인덱스를 넣는다.
        for (int i = 0; i < N; i++) {
            if (stack.isEmpty()) {
                stack.push(i);
            } else {
                while (!stack.isEmpty() && A[stack.peek()] < A[i]) {
                    result[stack.pop()] = A[i];
                }
                stack.push(i);
            }
        }



        // 결과 출력
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < N; i++) {
            sb.append(result[i]).append(' ');
        }
        System.out.println(sb);
    }
}
