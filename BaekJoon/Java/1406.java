import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Stack;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

        String initialStr = br.readLine();
        int M = Integer.parseInt(br.readLine());

        Stack<Character> leftStack = new Stack<>();
        Stack<Character> rightStack = new Stack<>();

        for (char c : initialStr.toCharArray()) {
            leftStack.push(c);
        }

        for (int i = 0; i < M; i++) {
            String command = br.readLine();
            // 로직 구현
            if (command.charAt(0) == 'L') {
                if (!leftStack.isEmpty()) {
                    rightStack.add(leftStack.pop());
                }
            } else if (command.charAt(0) == 'D') {
                if (!rightStack.isEmpty()) {
                    leftStack.add(rightStack.pop());
                }
            } else if (command.charAt(0) == 'B') {
                if (!leftStack.isEmpty()) {
                    leftStack.pop();
                }
            } else if (command.charAt(0) == 'P') {
                char toInsert = command.charAt(2);
                leftStack.push(toInsert);
            }
        }


        StringBuilder sb = new StringBuilder();
        while (!leftStack.isEmpty()) {
            sb.append(leftStack.pop());
        }
        sb.reverse();

        while (!rightStack.isEmpty()) {
            sb.append(rightStack.pop());
        }
        bw.write(sb.toString());
        bw.flush();
        bw.close();
        br.close();
    }
}
