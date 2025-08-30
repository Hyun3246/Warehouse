import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.StringTokenizer;
import java.util.Collections;
import java.util.LinkedList;
import java.util.Queue;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int N = Integer.parseInt(st.nextToken());
        int M = Integer.parseInt(st.nextToken());
        int V = Integer.parseInt(st.nextToken());


        ArrayList<ArrayList<Integer>> graph = new ArrayList<>(N + 1);
        for (int i = 0; i <= N; i++) {
            graph.add(new ArrayList<>());
        }
        
        // 간선 추가
        for (int i = 0; i < M; i++) {
            st = new StringTokenizer(br.readLine());
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            graph.get(a).add(b);
            graph.get(b).add(a);
        }

        // 그래프 각 정점의 인접 리스트를 오름차순으로 정렬
        for (int i = 0; i <= N; i++) {
            Collections.sort(graph.get(i));
        }

        // DFS
        boolean[] visited = new boolean[N + 1];
        StringBuilder sbDfs = new StringBuilder();
        dfs(graph, visited, V, sbDfs);
        System.out.println(sbDfs.toString());

        // BFS
        visited = new boolean[N + 1];
        StringBuilder sbBfs = new StringBuilder();
        bfs(graph, visited, V, sbBfs);
        System.out.println(sbBfs.toString());
    }

    private static void dfs(ArrayList<ArrayList<Integer>> graph, boolean[] visited, int node, StringBuilder sb) {
        visited[node] = true;
        sb.append(node).append(" ");
        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                dfs(graph, visited, neighbor, sb);
            }
        }
    }

        private static void bfs(ArrayList<ArrayList<Integer>> graph, boolean[] visited, int node, StringBuilder sb) {
        visited[node] = true;
        sb.append(node).append(" ");
        Queue<Integer> queue = new LinkedList<>();

        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                queue.offer(neighbor);
            }
        }

        while (!queue.isEmpty()) {
            int curr = queue.poll();
            if (!visited[curr]) {
                visited[curr] = true;
                sb.append(curr).append(" ");
                for (int neighbor : graph.get(curr)) {
                    if (!visited[neighbor]) {
                        queue.offer(neighbor);
                    }
                }
            }
        }
    }
}
