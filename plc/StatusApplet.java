/*
# This  program is free software; you may redistribute and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; Version 2.
# This guarantees your right to use, modify, and redistribute
# this software under certain conditions This program is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details at http://www.gnu.org/copyleft/gpl.html .
# The authors or our employer, will not be liable for any direct,
# indirect, special or consequential damages from the use of or
# failure to use of improper use of this tool.
# (Version 0.1, Venkat Pothamsetty, vpothams@cisco.com)
*/

import java.awt.*;
import javax.swing.*;
import javax.swing.text.*;
import javax.swing.event.*;
import java.util.*;
import java.net.*;
import java.io.*;
import java.awt.event.*;

import java.awt.event.MouseMotionListener;
import java.awt.event.MouseEvent;

public class StatusApplet extends JApplet
    implements MouseMotionListener, Runnable { //public class 
    

    //Net stuff
    public static String hostIP = "your hostname";
    public static int port = 502;
    public static ServerSocket hostServer = null;
    public static Socket socket = null;
    public static BufferedReader in = null;
    public static PrintWriter out = null;

    public final static boolean RIGHT_TO_LEFT = false;
    public static String testString = "testString";
    public static StatusApplet statusObj = new StatusApplet();

    //public static JFrame mainFrame = null;
    public final static JPanel mainPane = null;

    public static String GS = "Global Status";
    public static String OK = "OK";
    public static String GH = "Global Health";
    public static String CA = "Cable A";
    public static String CB = "Cable B";
    
    //Buttons for StatusField
    public static JButton gsButton = new JButton(GS);
    public static JButton ghButton = new JButton(GH);
    public static JButton caButton = new JButton(CA);
    public static JButton cbButton = new JButton(CB);
    
    //All OK Feilds, there should be a better way of doing this
    public  static JTextField okField1 = new JTextField(10); 
    public static JTextField okField2 = new JTextField(10); 
    public static JTextField okField3 = new JTextField(10);
    public static JTextField okField4 = new JTextField(10);

    //Buttons for Ethernet Feild
    public static JButton hostButton = new JButton("Hostname");
    public static JButton ipButton = new JButton("IP Address");
    public static JButton macButton = new JButton("MAC Address");
    public static JButton rackButton = new JButton("RACK");

    //Text for Ethernet Feild
    public static JTextField hnField = new JTextField(10); 
    public static JTextField ipField = new JTextField(10); 
    public static JTextField macField = new JTextField(10);
    public static JTextField rackField = new JTextField(10);
    
    //Buttons for Statistics Feild
    public static JButton trButton = new JButton("Transmits");
    public static JButton rcButton = new JButton("receives");
    public static JButton trErrorButton = new JButton("Transmit Errors");
    public static JButton rcErrorButton = new JButton("Receive Errors");
    public static JButton trCollisionButton = new JButton("Transmit Collisions");
    public static JButton rcCollisionButton = new JButton("Receive Collisoins");
    public static JButton trFlowButton = new JButton("Transmit Overflows");
    public static JButton rcFlowButton = new JButton("Receive Overflows");

    //Text for Statistics 
    public static JTextField trField = new JTextField(10); 
    public static JTextField rcField = new JTextField(10); 
    public static JTextField trErrorField = new JTextField(10); 
    public static JTextField rcErrorField = new JTextField(10); 
    public static JTextField trCollisionField = new JTextField(10); 
    public static JTextField rcCollisionField = new JTextField(10); 
    public static JTextField trFlowField = new JTextField(10); 
    public static JTextField rcFlowField = new JTextField(10); 

    //Text for Statistics Feild
    
    private static void initGUI(Container pane){
	JPanel statusPane = new JPanel();
	JPanel ethernetPane = new JPanel();
	JPanel statisticsPane = new JPanel();
	
	// Values for statusPane
	okField1.setText(OK); 	okField1.setEditable(true);
	okField2.setText(OK); 	okField2.setEditable(true);
	okField3.setText(OK); 	okField3.setEditable(true);
	okField4.setText(OK); 	okField4.setEditable(true);
	
	//Values for ethernetPane
	hnField.setText("PLC"); hnField.setEditable(true);
	ipField.setText("192.168.2.1"); ipField.setEditable(true);
	macField.setText("00:21:33:22:34:32"); macField.setEditable(true);
	rackField.setText("1"); rackField.setEditable(true);

	//Values for statisticsPane
	trField.setText("222"); trField.setEditable(true);
	rcField.setText("222"); rcField.setEditable(true);
	trErrorField.setText("444"); trErrorField.setEditable(true);
	rcErrorField.setText("555"); rcErrorField.setEditable(true); 
	trCollisionField.setText("666"); trCollisionField.setEditable(true);
	rcCollisionField.setText("777"); rcCollisionField.setEditable(true);
	trFlowField.setText("888"); trFlowField.setEditable(true);
	rcFlowField.setText("999"); rcFlowField.setEditable(true);

	statusPane = getStatusPane();
	ethernetPane = getEthernetPane();
	statisticsPane = getStatisticsPane();
	
	//You can add further panes here
	pane.add(statusPane,BorderLayout.NORTH);
	pane.add(ethernetPane,BorderLayout.CENTER);
	pane.add(statisticsPane,BorderLayout.SOUTH);
    }

    //The StatisticsPane is the pane whether the changing
    //statistics are displayed in the textfeilds.
    private static JPanel getStatisticsPane(){//get StatisticsPane
	JPanel tempPane = null;
	JPanel statisticsPane = new JPanel(new GridLayout(4, 2));
	ActionAdapter buttonListener = null;

	if (RIGHT_TO_LEFT) {
	    tempPane.setComponentOrientation(ComponentOrientation.RIGHT_TO_LEFT);
	}
	
	buttonListener = new ActionAdapter() {
		public void actionPerformed(ActionEvent e) {
		    System.out.println("trbutton pressed");
		    //connectBack("trbutton pressed");
		}
	    };
	
	trButton.addActionListener(buttonListener);
	
	Document doc = trField.getDocument();
	
	doc.addDocumentListener(
				new DocumentListener() {
				    public void changedUpdate(DocumentEvent e){
					System.out.println("Change");
					//connectBack("TextChanged");
					//you can call connectBack here
					// when text/attributes change...
				    }
				    public void insertUpdate(DocumentEvent e) {
					System.out.println("insert");
					// when text inserted...
					//connectBack("TextInserted");
				    }
				    public void removeUpdate(DocumentEvent e) {
       					System.out.println("remove");
					// when text removed...
					//connectBack("TextRemoved"); 
				    }
				});

	tempPane = new JPanel();
	
	trField.setText("TypeHere"); trField.setEditable(true);
	rcField.setText("222"); rcField.setEditable(true);
	trErrorField.setText("444"); trErrorField.setEditable(true);
	rcErrorField.setText("555"); rcErrorField.setEditable(true); 
	trCollisionField.setText("666"); trCollisionField.setEditable(true);
	rcCollisionField.setText("777"); rcCollisionField.setEditable(true);
	trFlowField.setText("888"); trFlowField.setEditable(true);
	rcFlowField.setText("999"); rcFlowField.setEditable(true);
	
	tempPane.setLayout(new GridLayout(3,4));

	tempPane.add(trButton);
	tempPane.add(trField);
	tempPane.add(rcButton);
	tempPane.add(rcField);
	tempPane.add(trErrorButton);
	tempPane.add(trErrorField);
	tempPane.add(trCollisionButton);
	tempPane.add(trCollisionField);
	tempPane.add(trFlowButton);
	tempPane.add(trFlowField);
	tempPane.add(rcFlowButton);
	tempPane.add(rcFlowField);
	
	statisticsPane.add(tempPane);
	return statisticsPane;
	
    }

    private static JPanel getEthernetPane(){//get StatisticsPane
	JPanel tempPane = null;
	JPanel ethernetPane = new JPanel(new GridLayout(2, 4));
	
	if (RIGHT_TO_LEFT) {
	    tempPane.setComponentOrientation(ComponentOrientation.RIGHT_TO_LEFT);
	}
	
	tempPane = new JPanel();
	
	//gsButton.addMouseMotionListener(this);
	//caButton.addMouseMotionListener(this);
	
	//tempPane.setLayout(new GridLayout(2,4));
	tempPane.add(hostButton);
	tempPane.add(hnField);
	tempPane.add(ipButton);
	tempPane.add(ipField);
	tempPane.add(macButton);
	tempPane.add(macField);
	tempPane.add(rackButton);
	tempPane.add(rackField);
	
	ethernetPane.add(tempPane);
	return ethernetPane;
	
    }
    
    private static JPanel getStatusPane(){ //get StatusPane
	
	JPanel tempPane = null;
	JPanel statusPane = new JPanel(new GridLayout(2, 4));
	ActionAdapter buttonListener = null;

	if (RIGHT_TO_LEFT) {
	    tempPane.setComponentOrientation(ComponentOrientation.RIGHT_TO_LEFT);
	}
	
	buttonListener = new ActionAdapter() {
		public void actionPerformed(ActionEvent e) {
		    System.out.println("cabbutton pressed");
		    //connectBack("cabbutton pressed");
		}
	    };

	caButton.addActionListener(buttonListener);
	
	tempPane = new JPanel();
	
	//tempPane.setLayout(new GridLayout(2,4));
	tempPane.add(gsButton);
	tempPane.add(okField1);
	tempPane.add(ghButton);
	tempPane.add(okField2);
	tempPane.add(caButton);
	tempPane.add(okField3);
	tempPane.add(cbButton);
	tempPane.add(okField4);
       

	statusPane.add(tempPane);
	return statusPane;
    } //getStatusPane()
    
    
    public void mouseMoved(MouseEvent e) {
	saySomething("Mouse moved", e);
    }
    
    public void mouseDragged(MouseEvent e) {
	saySomething("Mouse dragged", e);
    }
    
    void saySomething(String eventDescription, MouseEvent e) {
	System.out.println("Mouse Moved");
    }

    /**
     * Create the GUI and show it.  For thread safety,
     * this method should be invoked from the
     * event-dispatching thread.
     */
    private void createAndShowGUI() {


	Container mainPane = getContentPane();

	mainPane.setLayout(new GridLayout(2,1));

	statusObj =new StatusApplet();
	statusObj.initGUI(mainPane);
	
	try {
	    InetAddress addr = InetAddress.getLocalHost();
	    
	    // Get IP Address
	    byte[] ipAddr = addr.getAddress();
	    
	    // Get hostname
	    String hostname = addr.getHostName();
	    addr = InetAddress.getByAddress(ipAddr);
	    System.out.println(addr);
	    //connectBack(addr)
	    
	} catch (UnknownHostException e) {
	}

	System.out.println(this.getCodeBase().getHost());
	
	repaint();
	statusObj.run();	   
    }

    public static String generateRandom(){
	Random rand = new Random();

	// Random integers
	int i = rand.nextInt();
	
	return ((new Integer(i)).toString());
    }

    public void run() {
		
	//The thread sleeps for a while and continously calls
	// and displays random text.
	try{
	    Thread.sleep(1000);}
	catch (Exception x){x.printStackTrace();}
	
	String randString = generateRandom();
	//trField.setText(randString);
	randString = generateRandom();
	rcField.setText(randString);
	randString = generateRandom();
	trErrorField.setText(randString);
	randString = generateRandom();
	rcErrorField.setText(randString);
	randString = generateRandom();
	trCollisionField.setText(randString);
	randString = generateRandom();
	rcCollisionField.setText(randString);
	randString = generateRandom();
	trFlowField.setText(randString);
	randString = generateRandom();
	rcFlowField.setText(randString);
	repaint();
	
    }

    // Call this function when you want to get any information 
    //back.
    public static void connectBack(String myString){ //connectBack
	
	System.out.println("In connect back");
	String toSend = new String(myString);  
	String s = new String();
	
	
	try{
	    socket = new Socket(hostIP, port);
	} catch(Exception uhe){}

	try {
	    in = new BufferedReader(new 
				    InputStreamReader(socket.getInputStream()));
	    out = new PrintWriter(socket.getOutputStream(), true);
	}catch(IOException ioe)
	    {
	    }
	
	try{
	    // Send data
	    if (toSend.length() != 0) {
		out.print(toSend); out.flush();	 }
	    
	    // Receive data
	    if (in.ready()) {
		s = in.readLine();
		if ((s != null) &&  (s.length() != 0)) {
		    // Check if it is the end of a trasmission
		}
	    }
	} catch (IOException e){}
    }

    public void init(){
        //Schedule a job for the event-dispatching thread:
        //creating and showing this application's GUI.

	createAndShowGUI();
    }
}
