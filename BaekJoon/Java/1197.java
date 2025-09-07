import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.PriorityQueue;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int V = Integer.parseInt(st.nextToken());
        int E = Integer.parseInt(st.nextToken());

        ArrayList<LinkedList<Integer[]>> graph = new ArrayList<>(V + 1);
        boolean[] visited = new boolean[V + 1];

        for (int i = 1; i <= V + 1; i++) {
            graph.add(new LinkedList<Integer[]>());
        }

        // E개의 간선 정보를 입력받는 부분
        for (int i = 0; i < E; i++) {
            st = new StringTokenizer(br.readLine());
            int A = Integer.parseInt(st.nextToken());
            int B = Integer.parseInt(st.nextToken());
            int C = Integer.parseInt(st.nextToken());
            
            graph.get(A).add(new Integer[]{B, C});
            graph.get(B).add(new Integer[]{A, C});
        }

        long result = prim(graph, visited, 1);
    
        System.out.println(result);
    }

    private static long prim(ArrayList<LinkedList<Integer[]>> graph, boolean[] visited, int node) {
        long result = 0;
        PriorityQueue<Integer[]> heap = new PriorityQueue<>((o1, o2) -> o1[1] - o2[1]);
        int visitedCount = 0;

        heap.add(new Integer[]{node, 0});


        while (!heap.isEmpty()) {
            Integer[] curr = heap.poll();
            int currNode = curr[0];
            int currWeight = curr[1];

            if (visited[currNode]) {
                continue;
            }

            visited[currNode] = true;
            result += currWeight;
            visitedCount++;

            if (visitedCount == graph.size() - 1) {
                break;
            }

            for (Integer[] neighbor : graph.get(currNode)) {
                int nextNode = neighbor[0];
                if (!visited[nextNode]) {
                    heap.add(neighbor);
                }
            }
        }
        return result;
    }
}
