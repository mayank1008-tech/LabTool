import java.util.Scanner;
import java.util.StringTokenizer;

public class Toggle {
	public static void main(String[] args) {
		Scanner scn = new Scanner(System.in);
		System.out.print("Enter String:- ");
		String str = scn.nextLine();
		
		StringBuilder sb = new StringBuilder();
		
		for(char ch : str.toCharArray()){
			if(ch >='A'&& ch <= 'Z'){
				char toggled = (char)(ch - 'A' +'a');
				sb.append(toggled);
			}else if(ch >='a' && ch <='z'){
				char toggled = (char)(ch - 'a' + 'A');
				sb.append(toggled);
			}else{
				System.out.println("Enter a valid String!!!");
				return;
			}
		}
		
		System.out.println(sb);
		scn.close();
	}
}
