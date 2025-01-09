import java.util.*;


public class BPTNode {
	
	public List<Integer> keys;
	public List<BPTNode> children;
	public boolean isleafNode;
	public Map<Integer, Integer> keyAndValue;//leafNode면 key랑 value 쌍으로 저장 
	public BPTNode right;//leafNode면 오른쪽 sibling 가르켜야 함 
	public BPTNode parent;
	
	public BPTNode(boolean isleafNode) {
		this.isleafNode=isleafNode;
		keys=new ArrayList<>();
		children=new ArrayList<>();
		keyAndValue=new HashMap<>();
		right=null;
		parent=null;
	}
}
