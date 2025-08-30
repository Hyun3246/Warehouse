import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Stack;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String arrangement = br.readLine();
        
        // 여기에 로직을 구현해서 잘린 쇠막대기 조각의 총 개수를 계산

        Stack<Character> stack = new Stack<>();
        int result = 0;

        for (int i = 0; i < arrangement.length(); i++) {
            char current = arrangement.charAt(i);

            if (current == '(') {
                stack.push(current);
            } else {
                if (arrangement.charAt(i-1) == '(')  {
                    stack.pop();
                    result += stack.size();
                } else {
                    stack.pop();
                    result++;
                }
            }
        }

        // 최종 결과 출력
        System.out.println(result);
    }
}
