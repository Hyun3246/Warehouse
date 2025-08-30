import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.HashMap;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        int T = Integer.parseInt(br.readLine()); // 테스트 케이스의 수

        for (int i = 0; i < T; i++) {
            int n = Integer.parseInt(br.readLine()); // 의상의 수
            
            // 의상 종류를 key로, 해당 종류의 의상 개수를 value로 저장할 HashMap
            HashMap<String, Integer> clothes = new HashMap<>();

            for (int j = 0; j < n; j++) {
                st = new StringTokenizer(br.readLine());
                String name = st.nextToken(); // 의상 이름 (사용하지 않음)
                String type = st.nextToken(); // 의상 종류
                
                // 여기에 HashMap에 의상 종류별로 개수를 세는 로직 구현
                clothes.put(type, clothes.getOrDefault(type, 0) + 1);
            }

            // HashMap에 저장된 데이터를 바탕으로 조합의 수를 계산하는 로직
            int result = 1; // 아무것도 입지 않는 경우를 고려하여 1로 시작
            for (int count : clothes.values()) {
                result *= (count + 1); // 각 의상 종류별로 입지 않는 경우를 포함하여 경우의 수를 곱함
            }
            
            // 결과 출력
            System.out.println(result - 1); // 아무것도 입지 않는 경우를 제외
        }
    }
}
