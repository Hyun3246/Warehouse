import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.LinkedList;
import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.Arrays;

public class Main {
    final static int INF = 1_000_000_000;
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int V = Integer.parseInt(st.nextToken());
        int E = Integer.parseInt(st.nextToken());

        int K = Integer.parseInt(br.readLine());

        ArrayList<LinkedList<Integer[]>> graph = new ArrayList<>(V + 1);

        for (int i = 1; i <= V + 1; i++) {
            graph.add(new LinkedList<Integer[]>());
        }

        for (int i = 0; i < E; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            int w = Integer.parseInt(st.nextToken());

            graph.get(u).add(new Integer[]{v, w});
        }

        int[] allShortPath = dijkstra(graph, K);

        for (int i=1; i < V + 1; i++){
            if (allShortPath[i] == INF) {
                System.out.println("INF");
            }
            else{
                System.out.println(allShortPath[i]);
            }
            
        }
    }
    
    private static int[] dijkstra(ArrayList<LinkedList<Integer[]>> graph, int node) {

        int[] allShortPath = new int[graph.size()];

        Arrays.fill(allShortPath, INF);

        PriorityQueue<Integer[]> minHeap = new PriorityQueue<>((o1, o2) -> o1[1] - o2[1]);

        minHeap.add(new Integer[]{node, 0});
        allShortPath[node] = 0;

        while (!minHeap.isEmpty()) {
            Integer[] curr = minHeap.poll();
            int currNode = curr[0];
            int currWeight = curr[1];

            if (currWeight > allShortPath[currNode]) {
                continue;
            }

            for (Integer[] neighbor : graph.get(currNode)) {
                int nextNode = neighbor[0];
                int nextWeight = neighbor[1];
                if (allShortPath[currNode] + nextWeight < allShortPath[nextNode]) {
                    allShortPath[nextNode] = allShortPath[currNode] + nextWeight;
                    minHeap.add(new Integer[]{nextNode, allShortPath[currNode] + nextWeight});
                }
            }
        }

        return allShortPath;
    }
}
