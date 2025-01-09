import java.io.*;


public class Main {
	
	private static BPTree bptree;
	private static String indexFile;
	

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		if(args.length==0) {//명령이 없으면 에러 
			System.out.println("There is no command");
			return;
			
		}
		indexFile=args[1];
		switch(args[0]) {
			case "-c":
				if(args.length!=3) {
					return;
				}
				creation(Integer.parseInt(args[2]));
				break;
				
			case "-i":
				if(args.length!=3) {
					return;
				}
				insertion(args[2]);
				break;
			case "-d":
				if(args.length!=3) {
					return;
				}
				deletion(args[2]);
				break;
			case "-s":
				if(args.length!=3) {
					return;
				}
				singleKeySearch(Integer.parseInt(args[2]));
				break;
			case "-r":
				if(args.length!=4) {
					return;
				}
				rangedSearch(Integer.parseInt(args[2]), Integer.parseInt(args[3]));
				break;
			default:
				System.out.println("Wrong Command");
				break;
			
		}

	}
	
	private static void creation(int sizeOfNode) {
		bptree=new BPTree(sizeOfNode);
		bptree.saveTree(indexFile);
		System.out.println("IndexFile Creation Success");
		
	}
	private static void insertion(String inputFile) {
		
		bptree= new BPTree(0);
		bptree.loadTree(indexFile);
		
		try(BufferedReader br = new BufferedReader(new FileReader(inputFile))){
			String line;
			while((line=br.readLine())!=null) {
				String[] tmp=line.split(",");
				int key=Integer.parseInt(tmp[0]);
				int value=Integer.parseInt(tmp[1]);
				
				bptree.insert(key, value);
			}
			bptree.saveTree(indexFile);
			
			System.out.println("Insertion Success");
			
		}
		catch(IOException e) {
			System.out.println("Insertion Error "+e.getMessage());
		}
		
	}
	private static void deletion(String deleteFile) {
		bptree= new BPTree(0);
		bptree.loadTree(indexFile);
		
		try(BufferedReader br = new BufferedReader(new FileReader(deleteFile))){
			String line;
			while((line=br.readLine())!=null) {
				int key=Integer.parseInt(line);
				bptree.delete(key);
			}
			bptree.saveTree(indexFile);
			System.out.println("Deletion Success");
		}
		catch(IOException e) {
			System.out.println("Deletion Error "+e.getMessage());
		}

		
	}
	private static void singleKeySearch(int key) {
		bptree= new BPTree(0);
		bptree.loadTree(indexFile);
		
		if(bptree.findSingleKey(key)==false)System.out.println("NOT FOUND");
		
		else System.out.println("SingleKeySearch Success");
		
	}
	private static void rangedSearch(int startKey, int endKey) {
		bptree= new BPTree(0);
		bptree.loadTree(indexFile);
		
		if(bptree.findRangedKeys(startKey, endKey)==false)System.out.println("NOT FOUND");
		
		else System.out.println("RangedKey Success");
	}

}
