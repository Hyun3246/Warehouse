import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.ArrayList;
import java.util.LinkedList;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        // 컴퓨터의 수를 입력받는다.
        int n = Integer.parseInt(br.readLine());
        // 네트워크 상에 직접 연결되어 있는 컴퓨터 쌍의 수를 입력받는다.
        int m = Integer.parseInt(br.readLine());

        ArrayList<LinkedList<Integer>> network = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            network.add(new LinkedList<>());
        }

        // 네트워크 연결 정보를 처리하기 위한 반복문
        for (int i = 0; i < m; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            
            network.get(u).add(v);
            network.get(v).add(u);
        }


        int result = 0; // 결과 값을 저장할 변수

        boolean[] visited = new boolean[n + 1];
        dfs(1, network, visited);

        for (int i = 2; i <= n; i++) {
            if (visited[i]) {
                result++;
            }
        }

        System.out.println(result);
    }

    private static void dfs(int node, ArrayList<LinkedList<Integer>> network, boolean[] visited) {
        visited[node] = true;
        for (int neighbor : network.get(node)) {
            if (!visited[neighbor]) {
                dfs(neighbor, network, visited);
            }
        }
    }
}
