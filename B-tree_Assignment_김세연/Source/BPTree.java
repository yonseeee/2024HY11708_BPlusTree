import java.io.*;
import java.util.*;


public class BPTree {
	
	private BPTNode root;
	private int sizeOfNode;
	private BPTNode previousLeaf;
	private int minKey;
	
	public BPTree(int sizeOfNode) {
		root= new BPTNode(true);
		this.sizeOfNode=sizeOfNode;
		this.minKey=(int)(Math.ceil((this.sizeOfNode+1)/2.0))-1;
	}
	
	
	public BPTNode findLeafNode(int key) {//target key가 있는 leafNode 찾는 함수 
		BPTNode p=root;
		
		while(p.isleafNode==false) {
			int index=0;
			while(index<p.keys.size()&&key>=p.keys.get(index)) {
				index++;
			}
	
			p=p.children.get(index);
		}
		
		return p;
	}
	
	/*insertion에 필요한 함수*/

	public void insert(int key, int value) {
		BPTNode leafNode=findLeafNode(key);
		
		leafNode.keys.add(key);
		leafNode.keyAndValue.put(key, value);
		
		Collections.sort(leafNode.keys);
		
		if(leafNode.keys.size()>sizeOfNode)splitAndReorganizeLeafNode(leafNode);
		
	}
	
	public void splitAndReorganizeLeafNode(BPTNode leafNode) {
		
		BPTNode newNode= new BPTNode(true);
		int x=leafNode.keys.size()/2;
		
		for(int i=x;i<leafNode.keys.size();i++) {//기존node의 중간 지점 이후부터 newNode로 옮기기 
			Integer key=leafNode.keys.get(i);
			newNode.keys.add(key);
			
			newNode.keyAndValue.put(key, leafNode.keyAndValue.get(key));//key-value쌍 옮기기 
		}
		
		for(int i=leafNode.keys.size()-1;i>=x;i--) {//역순으로 지우기 
			Integer key=leafNode.keys.get(i);
			leafNode.keys.remove(i);
			leafNode.keyAndValue.remove(key);
			
		}
		
		newNode.parent=leafNode.parent;
		newNode.right=leafNode.right;
		leafNode.right=newNode;
		
		if(leafNode==root) {//split해야되는 노드가 root일 때는 root를 새로 만들어줘야함 
			BPTNode newRoot= new BPTNode(false);
			newRoot.keys.add(newNode.keys.get(0));
			newRoot.children.add(leafNode);
			newRoot.children.add(newNode);
			leafNode.parent=newRoot;
			newNode.parent=newRoot;
			root=newRoot;
		}else {//split해야되는 노드가 root가 아닐 때는 부모에 update 해줘야함  
			updateParent(leafNode, newNode.keys.get(0), newNode);
		}
	}
	public void updateParent(BPTNode node, int key, BPTNode newNode) {
		
		
		BPTNode parent=node.parent;
	    if (parent == null) {
	        // 새로운 루트 노드 생성
	        BPTNode newRoot = new BPTNode(false);
	        newRoot.keys.add(key);
	        newRoot.children.add(node);
	        newRoot.children.add(newNode);
	        node.parent = newRoot;
	        newNode.parent = newRoot;
	        root = newRoot;
	        return;
	    }
	    
		int i=0;
		while(i<parent.keys.size()&&key>=parent.keys.get(i)){
			i++;
		}
		parent.keys.add(i, key);
		parent.children.add(i+1, newNode);
		newNode.parent=parent; //
		
		if(parent.keys.size()>sizeOfNode) {
			splitAndReorganizeInternalNode(parent);
		}
		
	}
	
	public void splitAndReorganizeInternalNode(BPTNode node) {
		BPTNode newNode= new BPTNode(false);
		int x=node.keys.size()/2;
		int k=node.keys.get(x);
		
		for(int i=x+1;i<node.keys.size();i++) {//기존node의 중간 지점 이후부터 newNode로 옮기기 
			Integer key=node.keys.get(i);
			newNode.keys.add(key);
		}
		for(int i=x+1;i<node.children.size();i++) {//children 옮기기 
			BPTNode child=node.children.get(i);
			newNode.children.add(child);
			child.parent=newNode;
		}
		
		
		for(int i=node.keys.size()-1;i>=x;i--) {//기존 노드의 key 역순으로 지우기 
			node.keys.remove(i);
		}
		
		for(int i=node.children.size()-1;i>x;i--) {//기존 노드의 children 역순으로 지우기  
			node.children.remove(i);
		}

		if (node.children.size() > 0 && newNode.children.size() > 0) {
		    BPTNode leftChild = node.children.get(node.children.size() - 1);
		    BPTNode rightChild = newNode.children.get(0);
		    if (leftChild.isleafNode && rightChild.isleafNode) {
		        leftChild.right = rightChild;
		    }
		}
		newNode.parent=node.parent;
		
		if(node==root) {
			BPTNode newRoot=new BPTNode(false);
			newRoot.keys.add(k);
			newRoot.children.add(node);
			newRoot.children.add(newNode);
			node.parent=newRoot;
			newNode.parent=newRoot;
			root=newRoot;
		}else {
			updateParent(node, k, newNode);
		}
	}
	
	/*deletion에 필요한 함수들 */
	public void delete(int key) {
		BPTNode leafNode=findLeafNode(key);
		
		int index=leafNode.keys.indexOf(key);
		
		boolean flag=false;//맨 왼쪽 키인지 아닌
		if(index==0)flag=true;
		

		leafNode.keys.remove(index);

		leafNode.keyAndValue.remove(key);
		
	
		minKey=(int)(Math.ceil((this.sizeOfNode+1)/2.0))-1;
		
		if(leafNode==root) {
			if(leafNode.keys.size()<1) {
				System.out.println("The BPlusTree is deleted");
			}
		}
		else {
			if(leafNode.keys.size()<minKey&&flag==true) {
				deleteAndReorganize(leafNode);
				if(leafNode.right!=null)goUpandUpdate(leafNode, key, index);
			}
			else if(leafNode.keys.size()<minKey) {
				deleteAndReorganize(leafNode);
				
			}else if(flag==true) {
				goUpandUpdate(leafNode, key, index);
			}
		}
	}
	public void goUpandUpdate(BPTNode leafNode, int key, int nextIndex) {
		
		boolean flag=false;
		BPTNode parent=leafNode.parent;
		if(parent==null)return;
		
		int nextKey;
		if(leafNode.keys.size()==0) {
			nextKey = leafNode.right.keys.get(0);
		}
		else {
			nextKey=leafNode.keys.get(nextIndex);
		}
		
		
		while(parent!=null) {
			for(int i=0;i<parent.keys.size();i++) {
				if(parent.keys.get(i)==key) {
					parent.keys.remove(i);
					parent.keys.add(i, nextKey);
					
					flag=true;
					break;
				}
			}
			if(flag==false)break;
			parent=parent.parent;
		}

	}
	public void deleteAndReorganize(BPTNode node) {
		BPTNode parent=node.parent;
		
		if(parent==null)return; //root면 처리할 필요 없음 
		
		int index=parent.children.indexOf(node);
		
		int L=index-1;
		int R=index+1;
		
		if(index==0) {
			BPTNode rightNode=parent.children.get(R);
			if(rightNode.keys.size()==minKey) {
				merge(node, rightNode,parent, index);
			}
			else {
				borrowFromRight(parent, node, rightNode, index);
			}
		}
		else if(index==parent.children.size()-1) {
			BPTNode leftNode=parent.children.get(L);
			if(leftNode.keys.size()==minKey) {
				merge(leftNode, node, parent, index);
			}
			else {
				borrowFromLeft(parent, node, leftNode, index);
			}
		}
		else {
			BPTNode leftNode=parent.children.get(L);
			BPTNode rightNode=parent.children.get(R);
			if(leftNode.keys.size()==minKey&&rightNode.keys.size()==minKey) {
				merge(leftNode, node, parent, index);
			}
			else if(leftNode.keys.size()==minKey) {
				borrowFromRight(parent, node, rightNode, index);
			}
			else borrowFromLeft(parent, node, leftNode, index);
		}
	}
	public void borrowFromRight(BPTNode parent, BPTNode node, BPTNode rightNode, int index) {
		
		if(node.isleafNode==true) {
			int key=rightNode.keys.get(0);
			int value=rightNode.keyAndValue.get(key);
			
			node.keys.add(key);
			node.keyAndValue.put(key, value);
			
			parent.keys.remove(index);
			parent.keys.add(index, key);
			
			rightNode.keys.remove(0);
			rightNode.keyAndValue.remove(key);
		}
		else {
			BPTNode child=rightNode.children.get(0);
			child.parent=node;
			
			node.keys.add(parent.keys.get(index));
			node.children.add(child);
			
			parent.keys.remove(index);
			parent.keys.add(index,rightNode.keys.get(0));
			rightNode.keys.remove(0);
		}
		
	}
	public void borrowFromLeft(BPTNode parent, BPTNode node, BPTNode leftNode, int index) {
		if(node.isleafNode==true) {
			int key=leftNode.keys.get(leftNode.keys.size()-1);
			int value=leftNode.keyAndValue.get(key);
			
			node.keys.add(0, key);
			node.keyAndValue.put(key, value);
			
			parent.keys.remove(index-1);
			parent.keys.add(index-1, key);
			
			leftNode.keys.remove(leftNode.keys.size()-1);
		}
		else {
			BPTNode child=leftNode.children.get(leftNode.children.size()-1);
			child.parent=node;
			
			node.keys.add(0, parent.keys.get(index));
			node.children.add(child);
			
			parent.keys.remove(index-1);
			parent.keys.add(index-1,leftNode.keys.get(leftNode.keys.size()-1));
			leftNode.keys.remove(leftNode.keys.size()-1);
		}
		
	}
	
	public void merge(BPTNode leftNode, BPTNode rightNode, BPTNode parent, int index) {
		if(leftNode.isleafNode==true) {
			for(int i=0;i<rightNode.keys.size();i++) {
				Integer key= rightNode.keys.get(i);
				Integer value=rightNode.keyAndValue.get(key);
				leftNode.keys.add(key);
				leftNode.keyAndValue.put(key,value);
			}
			leftNode.right=rightNode.right;
		}
		else {
			leftNode.keys.add(parent.keys.get(index));
			for(int i=0;i<rightNode.keys.size();i++) {
				leftNode.keys.add(rightNode.keys.get(i));
			}
			for(int i=0;i<rightNode.children.size();i++) {
				rightNode.children.get(i).parent=leftNode;
				leftNode.children.add(rightNode.children.get(i));
			}
		}
		if(leftNode.isleafNode==true&&index==parent.keys.size()) {
			parent.keys.remove(index-1);
		}
		else parent.keys.remove(index);
		
		parent.children.remove(rightNode);
		
		if(parent==root&&parent.keys.size()==0) {
			root=leftNode;
			leftNode.parent=null;
		}
		else if(parent.keys.size()<minKey) {
			deleteAndReorganize(parent);
		}
		
	}

	/*singleKey 찾는 함수 */
	public boolean findSingleKey(int key){
		
		boolean ifFound=false;
		BPTNode p=root;
		
		while(p.isleafNode==false) {
			int index=0;
			while(index<p.keys.size()&&key>=p.keys.get(index)) {//size제한 ****
				index++;
			}
			for(int i=0;i<p.keys.size();i++) {
				System.out.print(p.keys.get(i));
				if(i!=p.keys.size()-1)System.out.print(",");
			}
			System.out.println();
			
			p=p.children.get(index);
		}
		for(int i=0;i<p.keys.size();i++) {
			if(key==p.keys.get(i)) {
				System.out.println(p.keyAndValue.get(key));
				ifFound=true;
				
			}
		}
		
		return ifFound;
	}
	
	
	/*rangedKeys찾는 함수*/
	public boolean findRangedKeys(int startKey, int endKey) {
		BPTNode p=findLeafNode(startKey);
		
		boolean flag=false;
		while(p!=null) {
			for(int i=0;i<p.keys.size();i++) {
				Integer key=p.keys.get(i);
				if(key>=startKey && key<=endKey)
					flag=true;
					System.out.println(key+","+p.keyAndValue.get(key));
			}
			p=p.right;
		}
		
		return flag;
	}
	
	
	/*index 파일 저장하고 불러오는데 필요한 함수들 */
	
	public void saveTree(String indexFile) {
		try(BufferedWriter bw = new BufferedWriter(new FileWriter(indexFile))){
			
			bw.write(Integer.toString(sizeOfNode));
			bw.newLine();
			
			saveNode(bw, root);
			System.out.println("Tree is saved");
		}
		catch (IOException e) {
            System.out.println("Saving Error: " + e.getMessage());
        }
	}
	public void saveNode(BufferedWriter bw, BPTNode node)throws IOException{
		if(node.isleafNode==true)bw.write(Integer.toString(1));
		else bw.write(Integer.toString(0));
		bw.newLine();
		
		for(int i=0;i<node.keys.size();i++) {
			String key=Integer.toString(node.keys.get(i));
			bw.write(key);
			if(i!=node.keys.size()-1)bw.write(",");
		}
		bw.newLine();
		
		if(node.isleafNode==true) {
			for(int i=0;i<node.keys.size();i++) {
				Integer key=node.keys.get(i);
				Integer value=node.keyAndValue.get(key);
				
				bw.write(Integer.toString(key)+","+Integer.toString(value));
				bw.newLine();
			}
		}else {
			for(int i=0;i<node.children.size();i++) {
				saveNode(bw, node.children.get(i));
			}
		}
	}
	public void loadTree(String indexFile) {
		
		previousLeaf=null;
		try(BufferedReader br = new BufferedReader(new FileReader(indexFile))){
			
			String size=br.readLine();
			sizeOfNode=Integer.parseInt(size);
			root=loadNode(br);
			System.out.println("Tree is loaded");
		}
		catch (IOException e) {
	        System.out.println("Loading Error " + e.getMessage());
	    }
	}
	public BPTNode loadNode(BufferedReader br)throws IOException{
		String nodeType=br.readLine();
		boolean isLeafNode=nodeType.equals("1");
		BPTNode node = new BPTNode(isLeafNode);
		
		String keysLine = br.readLine();
		
		if(keysLine!=null&&!keysLine.isEmpty()) {//파일의 끝이거나 keyline이 비어있지 않으면 
			String[] tmp=keysLine.split(",");
	
			for(String key : tmp) {//tmp.length()로 해보
				node.keys.add(Integer.parseInt(key));
			}
		}
		if(isLeafNode==true) {
			for(int i=0;i<node.keys.size();i++) {
				String keyValueLine=br.readLine();
				String[]tmp=keyValueLine.split(",");
				node.keyAndValue.put(Integer.parseInt(tmp[0]), Integer.parseInt(tmp[1]));
			}
			if(previousLeaf!=null) {
				previousLeaf.right=node;
			}
			previousLeaf=node;
		}
		else {
			for(int i=0;i<=node.keys.size();i++) {
				BPTNode child=loadNode(br);
				child.parent=node;
				node.children.add(child);
			}
		}
		
		return node;
	}
}
