# Auction System  
## 1. Introduction 
The project consists of designing and implementing an auction system (AS) which offers its services as SaaS to end-users who can offer items for auction and bid for items. The high- level description of the system to implement is given in Section 2 while the requirements are stated in Section 3.  
## 2. Auction System Protocol Description 
The Auction System (AS) resides in the cloud for scalability and elasticity purpose. The AS allows for the end-users to register. Only registered end-users are allowed to offer items for auction and bid. A registered end-user can advertise many items for sale at a time. Auctions for an item are open during 5 minutes after its advertising and the broadcasting of the information to all registered end-users. An item is sold to the highest bid at the end of the period of 5 minutes. For every item, the AS keeps informing the end-users about the current highest bid. An end-user can bid as many times as she/he wishes for an item on auction.  
### 2.1 Registering with the AS 
An end-user has a unique Name. The AS has to keep this information. An end-user can always try to leave the Auction System. However, she/he can be denied deregistration if she/he is currently offering an item for auction or active in bidding for at least one item (currently leading with the highest bid for at least one item)  
### 2.2 Offering items for auction 
Every registered end-user can offer items for sale.  
### 2.3 Bidding for items 
An end-user can bid on any item being currently offered and can submit as many items as she/he wishes. To keep the end-users informed on every item, any change in the current highest bid is sent to all the registered end-users. When the bidding period of 5 minutes is over, the AS informs the winning users. If there is more than one end-user with the highest bid, the first bid to reach the AS wins. The AS also informs the end-user who is selling the item about the winner. When an item has not attracted a single valid bid, the AS restarts the bidding process for another period of 5 minutes. This can be repeated until an end-user makes a winning bid.  
## 3 Requirements 
<ul> 
  <li>Projects should be done in teams.</li>   
  <li>Each student should select and motivate the cloud technologies (e.g. PaaS, IaaS)she/he uses in the project.</li>   
  <li>The expected output consists of:</li>   
  <ul>     
    <li>A technical report (max: 10 pages).</li>     
    <li>A powerpoint presentation (5 minutes) to introduce your demo</li>     
    <li>A live demo</li>   
   </ul> 
</ul>
