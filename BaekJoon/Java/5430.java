import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        int T = Integer.parseInt(br.readLine());

        testCaseLoop: 
        for (int i = 0; i < T; i++) {
            String p = br.readLine();
            int n = Integer.parseInt(br.readLine());
            String arrStr = br.readLine();


            Deque<Integer> deque = new ArrayDeque<>();
            

            String content = arrStr.substring(1, arrStr.length() - 1);
            if (n > 0) { 
                String[] elements = content.split(","); 
                for (String element : elements) {
                    deque.add(Integer.parseInt(element));
                }
            }


            boolean isReversed = false;

            for (char command : p.toCharArray()) {
                if (command == 'R') {
                    isReversed = !isReversed; 
                } else { // 'D' 연산
                    // 4. 에러 처리
                    if (deque.isEmpty()) {
                        sb.append("error\n");
                        continue testCaseLoop;
                    }
                    
                    if (isReversed) {
                        deque.removeLast(); 
                    } else {
                        deque.removeFirst(); 
                    }
                }
            }

            // 5. 최종 출력 형식 맞추기
            sb.append('[');
            if (!deque.isEmpty()) {
                if (isReversed) { 
                    while (deque.size() > 1) {
                        sb.append(deque.removeLast()).append(',');
                    }
                    sb.append(deque.removeLast());
                } else { 
                    while (deque.size() > 1) {
                        sb.append(deque.removeFirst()).append(',');
                    }
                    sb.append(deque.removeFirst());
                }
            }
            sb.append("]\n");
        }
        System.out.print(sb);
    }
}
