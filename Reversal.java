import java.util.Scanner;
import java.util.Stack;

public class Reversal {
    public static void main(String[] args) {
        Stack<Character> st = new Stack<>();
        Scanner scn = new Scanner(System.in);
        System.out.print("Enter the string:- ");
        String str = scn.nextLine();

        for(char c : str.toCharArray()){
            st.push(c);
        }
        String ans = "";
        while(!st.isEmpty()){
            ans += st.pop();
        }
        System.out.println("Reversed String is:- "+ans);
        scn.close();
    }
}
