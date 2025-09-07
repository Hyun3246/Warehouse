import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int N = Integer.parseInt(br.readLine());
        ArrayList<LinkedList<Integer>> graph = new ArrayList<>(N + 1);
        int[] parent = new int[N + 1];
        boolean[] visited = new boolean[N + 1];

        for (int i = 1; i <= N + 1; i++) {
            graph.add(new LinkedList<Integer>());
        }

        for (int i = 0; i < N - 1; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            graph.get(a).add(b);
            graph.get(b).add(a);
        }

        bfs(graph, visited, 1, parent);

        for (int i = 2; i < N + 1; i++){
            System.out.println(parent[i]);
        }

    }

    public static void bfs(ArrayList<LinkedList<Integer>> graph, boolean[] visited, int node, int[] parent) {
        visited[node] = true;
        Queue<Integer> nextVisit = new LinkedList<>();
        for (int neighbor : graph.get(node)) {
            nextVisit.offer(neighbor);
            parent[neighbor] = node;
        }

        while (!nextVisit.isEmpty()) {
            int curr = nextVisit.poll();
            if (!visited[curr]) {
                visited[curr] = true;
                for (int neighbor : graph.get(curr)) {
                    if (!visited[neighbor]) {
                        nextVisit.offer(neighbor);
                        parent[neighbor] = curr;
                    }
                }
            }

        }
    }
}
