import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.LinkedList;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine(), " ");

        int N = Integer.parseInt(st.nextToken()); // 큐의 크기
        int M = Integer.parseInt(st.nextToken()); // 뽑으려는 수의 개수

        st = new StringTokenizer(br.readLine(), " ");
        int[] targets = new int[M];
        for (int i = 0; i < M; i++) {
            targets[i] = Integer.parseInt(st.nextToken());
        }

        // 여기에 큐(덱)를 생성하고 1부터 N까지의 원소를 넣는 초기화 로직
        LinkedList<Integer> deque = new LinkedList<>();

        for (int i = 1; i <= N; i++) {
            deque.add(i);
        }

        int count = 0; // 2번, 3번 연산의 총 횟수


        for (int i = 0; i < M; i++) {
            int index = deque.indexOf(targets[i]);
            int rotateLeft = index;
            int rotateRight = deque.size() - index;
            count += Math.min(rotateLeft, rotateRight);
            if (rotateRight < rotateLeft) {
                for (int j = 0; j < rotateRight; j++) {
                    int temp = deque.pollLast();
                    deque.addFirst(temp);
                }
            } else {
                for (int j = 0; j < rotateLeft; j++) {
                    int temp = deque.pollFirst();
                    deque.addLast(temp);
                }
            }
            deque.pollFirst(); // 뽑기
        }

        // 최종 결과(2번, 3번 연산 횟수의 총합) 출력
        System.out.println(count);
    }
}
