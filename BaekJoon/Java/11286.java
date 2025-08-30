import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Comparator;
import java.util.PriorityQueue;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int N = Integer.parseInt(br.readLine());
        
        // 람다식을 이용해서 비교 조건을 직접 지정
        PriorityQueue<Integer> minHeap = new PriorityQueue<>((a, b) -> {
            int absA = Math.abs(a);
            int absB = Math.abs(b);

            if (absA == absB) {
                return a - b;
            } else {
                return absA - absB;
            }
        });

        for (int i = 0; i < N; i++) {
            int x = Integer.parseInt(br.readLine());

            if (x == 0) {
                // 배열에서 가장 작은 값을 출력하고 그 값을 제거하는 로직
                if (minHeap.isEmpty()) {
                    System.out.println(0);
                } else {
                    System.out.println(minHeap.poll());
                }
            } else {
                // 배열에 x라는 값을 넣는 로직
                minHeap.add(x);
            }
        }
    }
}
