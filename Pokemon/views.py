# Create your views here.
import random
import json
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import datetime
import sqlalchemy
from sqlalchemy import text, DDL
#from pyecharts import options as opts
#from pyecharts.charts import Bar
#trigger = "CREATE TRIGGER bonus1 BEFORE INSERT ON BoxOrder FOR EACH ROW BEGIN SET @totalBuy = (select count(b_orderID) from BoxOrder where boxID = NEW.boxID group by userID having userID = NEW.userID); IF(@totalBuy >= 5) THEN SET NEW.pay_amount = NEW.pay_amount * 0.9; END IF; END;"
cursor = connection.cursor()
cursor.execute(" drop trigger if exists bonus1;")
cursor.execute("CREATE TRIGGER bonus1 "
               "BEFORE INSERT ON BoxOrder "
               "FOR EACH ROW "
               "BEGIN SET @totalBuy = (select count(b_orderID) "
               "from BoxOrder "
               "where boxID = NEW.boxID and datediff(STR_TO_DATE(NEW.pay_datetime,'%Y%m%d'),STR_TO_DATE(pay_datetime,'%Y%m%d')) <= 10 "
               "group by userID "
               "having userID = NEW.userID); "
               "IF(@totalBuy >= 5) THEN "
               "SET NEW.pay_amount = NEW.pay_amount * 0.9; "
               #"UPDATE BoxOrder SET pay_amount = NEW.pay_amount * 0.9 WHERE b_orderID = new.b_orderID; "
                "IF(@totalBuy >= 10) THEN "
               "SET @bonuscard = (select cardNo from Card where rarity = 'B' order by RAND() limit 1);"
               "Insert into OwnedCard(cardNo, userID, status,c_price) values(@bonuscard, NEW.userID, 'bonus', 0.0); "
                "END IF; "
               "END IF; "
               "END;" )

cursor.execute("DROP PROCEDURE  IF EXISTS bonus2;")
#cursor.execute("create procedure bonus2(IN HP int(10),IN MP int(10),IN LP int(10))begin     declare uid INT(16); declare cardno1 INT(16); declare totalprice decimal(10,2); declare totalbox INT(16); declare rare VARCHAR(50); declare exp_num VARCHAR(50); declare nor_num VARCHAR(50); declare ch_num VARCHAR(50);	 declare done int default FALSE; declare cur cursor for (select  userID from User natural join BoxOrder group by userID order by userID); declare continue handler for not FOUND set done=TRUE;     drop table if exists bonustable; create table bonustable(        userID INT(16), totalprice DECIMAL(10,2), exp_num INT(16), nor_num INT(16), ch_num INT(16), rare varchar(10), cardno INT(16) );		 open cur; CLOOP:loop fetch cur into uid; if done then LEAVE CLOOP; end if; select sum(b_price) into totalprice from BoxOrder NATURAL join BlindBox where userID = uid  and datediff(CURRENT_DATE,STR_TO_DATE(pay_datetime,'%Y%m%d'))<=7 ;					 select COUNT(b_orderID) into exp_num from BoxOrder natural join (        select b_orderID,b_price, case  WHEN b_price > 70 THEN 'H' WHEN b_price > 30 THEN 'M' ELSE 'L' END AS order_level from BoxOrder natural join BlindBox ) b WHERE datediff(CURRENT_DATE,STR_TO_DATE(pay_datetime,'%Y%m%d'))<=7  and userID = uid  and order_level='H';						 select COUNT(b_orderID) into nor_num from BoxOrder natural join (        select b_orderID,b_price, case  WHEN b_price > 70 THEN 'H' WHEN b_price > 30 THEN 'M' ELSE 'L' END AS order_level from BoxOrder natural join BlindBox ) b WHERE datediff(CURRENT_DATE,STR_TO_DATE(pay_datetime,'%Y%m%d'))<=7  and userID = uid  and order_level='M';						 select COUNT(b_orderID) into ch_num from BoxOrder natural join ( select b_orderID,b_price, case  WHEN b_price > 70 THEN 'H' WHEN b_price > 30 THEN 'M' ELSE 'L' END AS order_level from BoxOrder natural join BlindBox ) b WHERE datediff(CURRENT_DATE,STR_TO_DATE(pay_datetime,'%Y%m%d'))<=7  and userID = uid  and order_level='L';						 if totalprice >=HP and (exp_num >=3 or nor_num >=5 or  ch_num >=7) then set rare = 'B';             elseif totalprice >=MP and (exp_num >=1 or nor_num >=3 or  ch_num >=5)then set rare = 'C';						 elseif totalprice >=LP then set  rare = 'D'; else  set rare=''; end if;						 if rare!='' then select cardNo  into cardno1 from Card where rarity = rare order by RAND() limit 1; Insert into bonustable values(uid,totalprice,exp_num,nor_num,ch_num,rare,cardno1);						 Insert into OwnedCard(cardNo, userID, status,c_price) values(cardno1, uid, 'send', 0.0); end if; END LOOP CLOOP; close cur; select * from bonustable order by rare; end;")
#cursor.execute("create procedure bonus2(IN HP int(10),IN MP int(10),IN LP int(10)) begin  declare uid INT(16);declare cardno1 INT(16);declare totalprice decimal(10,2);declare avgprice1 decimal(10,2);declare totalbox INT(16);declare rare VARCHAR(50);declare exp_num VARCHAR(50);declare nor_num VARCHAR(50);declare ch_num VARCHAR(50);declare favor_type VARCHAR(50);declare done int default FALSE;declare cur cursor for (select  userID from User natural join BoxOrder group by userID order by userID);declare continue handler for not FOUND set done=TRUE;  drop table if exists bonustable;create table bonustable(userID INT(16),totalprice DECIMAL(10,2),exp_num INT(16),nor_num INT(16),ch_num INT(16),rare varchar(10),cardno INT(16),favroite_cardtype VARCHAR(50));		open cur;CLOOP:loop fetch cur into uid;if done then LEAVE CLOOP;end if;select sum(b_price)into totalprice from BoxOrder NATURAL join BlindBox where userID = uid and datediff(CURRENT_DATE,STR_TO_DATE(pay_datetime,'%Y%m%d'))<=7 ;	select count(c.H) AS HP,count(c.M) AS MP,count(c.L) AS LPinto exp_num,nor_num,ch_num from  (select case order_level when 'H' then b_orderID end as H,case order_level when 'M' then b_orderID end as M,case order_level when 'L' then b_orderID end as L	from BoxOrder natural join (select b_orderID,b_price,  case  WHEN b_price > 70 THEN 'H' WHEN b_price > 30 THEN 'M' ELSE 'L' END AS order_level from BoxOrder natural join BlindBox )b WHERE datediff(CURRENT_DATE,STR_TO_DATE(pay_datetime,'%Y%m%d'))<=7 and userID = uid ) c;	select type into favor_type from OwnedCard natual join Card where userID=uid group by type order by count(cardID) desc limit 1;	if totalprice >=HP and (exp_num >=3 or nor_num >=5 or  ch_num >=7) then set rare = 'B';          elseif totalprice >=MP and (exp_num >=1 or nor_num >=3 or  ch_num >=5)then set rare = 'C'; elseif totalprice >=LP then set  rare = 'D';else set rare='';end if;if rare!='' then select cardNo into cardno1 from Card where rarity = rare order by RAND()limit 1; Insert into bonustable values(uid,totalprice,exp_num,nor_num,ch_num,rare,cardno1,favor_type);	Insert into OwnedCard(cardNo, userID, status,c_price)values(cardno1, uid, 'bonus', 0.0);						end if;END LOOP CLOOP;close cur;select * from bonustableorder by rare ;       end;")
cursor.execute("create procedure bonus2(IN HP int(10),IN MP int(10),IN LP int(10))"
"begin"
"    declare uid INT(16);"
"    declare cardno1 INT(16);"
"    declare totalprice decimal(10,2);"
"		declare avgprice1 decimal(10,2);"
"    declare totalbox INT(16);"
"    declare rare VARCHAR(50);"
"		declare exp_num VARCHAR(50);"
"		declare nor_num VARCHAR(50);"
"		declare ch_num VARCHAR(50);"
"  	declare favor_type VARCHAR(50);"
"    declare done int default FALSE;"
"    declare cur cursor for (select  userID from User natural join BoxOrder group by userID order by userID);"
"     declare continue handler for not FOUND set done=TRUE; "
"		drop table if exists bonustable;"
"		create table bonustable("
"		userID INT(16),"
"		totalprice DECIMAL(10,2),"
"		exp_num INT(16),"
"		nor_num INT(16),"
"		ch_num INT(16),"
"		rare varchar(10),"
"		cardno INT(16),"
"		favroite_cardtype VARCHAR(50)"
"		);		"
"    open cur;"
"    CLOOP:loop"
"            fetch cur into uid;"
"            if done then"
"            LEAVE CLOOP;"
"            end if;"
"            select sum(b_price)"
"            into totalprice"
"            from BoxOrder NATURAL join BlindBox"
"            where userID = uid "
"						and datediff(CURRENT_DATE,STR_TO_DATE(pay_datetime,'%Y%m%d'))<=7 ;											"
"	select count(c.H) AS HP,count(c.M) AS MP,count(c.L) AS LP"
"    into exp_num,nor_num,ch_num"
"	from"
"	(select case order_level when 'H' then b_orderID end as H,"
"	case order_level when 'M' then b_orderID end as M,"
"	case order_level when 'L' then b_orderID end as L	"
"						from BoxOrder natural join ("
"						select b_orderID,b_price,"
"						case  WHEN b_price > 70 THEN 'H' "
"						WHEN b_price > 30 THEN 'M'"
"						ELSE 'L'"
"						END AS order_level"
"						from BoxOrder natural join BlindBox"
"						) b"
"						WHERE datediff(CURRENT_DATE,STR_TO_DATE(pay_datetime,'%Y%m%d'))<=7 "
"					  and userID = uid	)c;						"
"						select type"
"						into favor_type"
"						from OwnedCard natual join Card"
"						where userID=uid"
"						group by type"
"						order by count(cardID) desc"
"						limit 1;"
"						if totalprice >=HP and (exp_num >=3 or nor_num >=5 or  ch_num >=7) then"
"            set rare = 'B';"
"						elseif totalprice >=MP and (exp_num >=1 or nor_num >=3 or  ch_num >=5)then"
"            set rare = 'C';	"
"					  elseif totalprice >=LP then"
"						set  rare = 'D';"
"						else "
"						set rare='';"
"						end if;"
"						if rare!='' then"
"						select cardNo "
"            into cardno1"
"            from Card"
"            where rarity = rare"
"            order by RAND()"
"            limit 1;		"
"						Insert into bonustable"
"            values(uid,totalprice,exp_num,nor_num,ch_num,rare,cardno1,favor_type);"
"						"
"						Insert into OwnedCard(cardNo, userID, status,c_price)"
"					values(cardno1, uid, 'bonus', 0.0);"
"						"
"						end if;"
"        END LOOP CLOOP;"
"			  close cur;"
"				select * from bonustable"
"				order by rare ;"
"end;")
def login(request):
    if request.session.get('is_login', None):
        return redirect('/mainpage/')

    else:
        if request.method == "POST":
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            message = ""

            if username and password:
                username = username.strip()
                cursor = connection.cursor()
                cursor.execute("select * from User where u_name=%s limit 1", username)
                #cursor.execute(trigger)
                result = cursor.fetchone()

                if result[1] == password:
                    message = 'password match'
                    request.session['username'] = username
                    request.session['userID'] = result[0]
                    request.session['is_login'] = True
                    if username == 'admin':
                        return redirect('/adminpage/')
                    return redirect('/mainpage/')
                else:
                    message = "password not correct！"
            else:
                message = "Please enter both username and Password"

            return render(request, 'login.html', {"message": message})
        else:
            return render(request, 'login.html')

def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
        return redirect("/login/")


def mainpage(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        cursor.execute("select * from BlindBox")
        blindboxlist = cursor.fetchall()
        return render(request, 'mainpage.html', {'blindboxlist': blindboxlist})
    else:
        return redirect('/login/')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        passwordconfirm = request.POST.get('passwordconfirm', None)
        message = ""

        if username and password and passwordconfirm:
            if passwordconfirm == password:
                cursor = connection.cursor()
                cursor.execute("Select * from User where u_name= %s", username)
                is_existed = cursor.fetchall()
                if not is_existed:
                    cursor.execute("Insert into User (password,u_name) values(%s,%s)", [password, username])
                    return redirect("/login/")
                else:
                    message = "This username already exists, please change another one"
            else:
                message = "Password doesn't match"
        else:
            message = "you should enter all of the fields"

        return render(request, 'signup.html', {"message": message})
    else:
        return render(request, 'signup.html')


def mypokemon(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        userID = request.session.get('userID', None)
        cursor.execute("select c_name,rarity, img,type,status,cardID from Card natural join OwnedCard where userID =%s order by cardID desc ",
                       userID)
        cardlist = cursor.fetchall()
        return render(request, 'mypokemon.html', {'cardlist': cardlist})
    else:
        return redirect('/login/')

def checkbox(request):
    if request.method == "POST":
        cursor = connection.cursor()
        typefilter = request.POST.get('typefilter', None)
        price = request.POST.get('price', None)
        types = request.POST.getlist('type', None)

        if price == 'less40':
            if typefilter == 'alltypes' or len(types) == 0:
                cursor.execute(
                    "select * from BlindBox where b_price < 40"
                )
            else:
                if len(types) == 1:
                    cursor.execute(
                        "select * from BlindBox where (b_price < 40 and title = %s)", types[0]
                    )
                if len(types) == 2:
                    cursor.execute(
                        "select * from BlindBox where (b_price < 40 and (title = %s or title = %s))", [types[0], types[1]]
                    )
                if len(types) == 3:
                    cursor.execute(
                        "select * from BlindBox where (b_price < 40 and (title = %s or title = %s or title = %s))", [types[0], types[1], types[2]]
                    )

        else:
            if typefilter == 'alltypes' or len(types) == 0:
                cursor.execute(
                    "select * from BlindBox where b_price >= 40"
                )
            else:
                if len(types) == 1:
                    cursor.execute(
                        "select * from BlindBox where (b_price >= 40 and title = %s)", types[0]
                    )
                if len(types) == 2:
                    cursor.execute(
                        "select * from BlindBox where (b_price >= 40 and (title = %s or title = %s))", [types[0], types[1]]
                    )
                if len(types) == 3:
                    cursor.execute(
                        "select * from BlindBox where (b_price >= 40 and (title = %s or title = %s or title = %s))", [types[0], types[1], types[2]]
                    )
        boxlist = cursor.fetchall()
        return render(request, 'mainpage.html', {'blindboxlist': boxlist})

def boxhistory(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        userID = request.session.get('userID', None)
        cursor.execute(
            "select b_orderID, title ,pay_amount,pay_datetime from BoxOrder natural join BlindBox where userID =%s order by b_orderID desc",
            userID)
        boxhistorylist = cursor.fetchall()
        return render(request, 'boxhistory.html', {'boxhistorylist': boxhistorylist})
    else:
        return redirect('/login/')


def buyonebox(request):
    boxid = request.POST.get('boxid')
    userid = request.session.get('userID', None)
    if userid == 20:
        return redirect('/mainpage/')
    today = datetime.date.today()
    paydate = today.strftime('%Y%m%d')
    cursor = connection.cursor()


    cursor.execute("select b_price from BlindBox where boxID =%s", boxid)
    price = cursor.fetchone()
    price = price[0]

    cursor.execute("select title, rarity, prob from BlindBox natural join Probability where boxID = %s", boxid)
    box_pro = []
    for i in range(4):
        box_infor = cursor.fetchone()
        box_pro.append(box_infor[2])

    returnlist = []
    for i in range(5):
        m = random.randint(1, 1000)
        if box_infor[0] == 'Fire' or box_infor[0] == 'Water' or box_infor[0] == 'Grass':
            if m <= box_pro[0] * 1000:
                cursor.execute(
                    "select cardNo,img ,c_name from Card where type = %s and rarity = %s order by Rand() limit 1",
                    [box_infor[0], 'A'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]

                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'A', card_infor[1]])

            elif m <= (box_pro[0] + box_pro[1]) * 1000:
                cursor.execute(
                    "select cardNo,img ,c_name from Card where type = %s and rarity = %s order by Rand() limit 1",
                    [box_infor[0], 'B'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'B', card_infor[1]])
            elif m <= (box_pro[0] + box_pro[1] + box_pro[2]) * 1000:
                cursor.execute(
                    "select cardNo,img ,c_name from Card where type = %s and rarity = %s order by Rand() limit 1",
                    [box_infor[0], 'C'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'C', card_infor[1]])
            else:
                cursor.execute(
                    "select cardNo,img ,c_name from Card where type = %s and rarity = %s order by Rand() limit 1",
                    [box_infor[0], 'D'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'D', card_infor[1]])
        else:
            if m <= box_pro[0] * 1000:
                cursor.execute("select cardNo,img ,c_name from Card where rarity = %s order by Rand() limit 1",
                               ['A'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'A', card_infor[1]])

            elif m <= (box_pro[0] + box_pro[1]) * 1000:
                cursor.execute("select cardNo,img ,c_name from Card where rarity = %s order by Rand() limit 1",
                               ['B'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'B', card_infor[1]])
            elif m <= (box_pro[0] + box_pro[1] + box_pro[2]) * 1000:
                cursor.execute("select cardNo,img ,c_name from Card where rarity = %s order by Rand() limit 1",
                               ['C'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'C', card_infor[1]])
            else:
                cursor.execute("select cardNo,img ,c_name from Card where rarity = %s order by Rand() limit 1",
                               ['D'])
                card_infor = cursor.fetchone()
                cardNo = card_infor[0]
                cursor.execute("Insert into OwnedCard (cardNo,userID,status,c_price) values(%s,%s,%s,%s)",
                               [cardNo, userid, 'owned', 0.0])
                returnlist.append([card_infor[2], 'D', card_infor[1]])

    cursor.execute(
        "Insert into BoxOrder (userID,boxID,pay_datetime,pay_amount) values(%s,%s,%s,%s);",
        [userid, int(boxid), paydate, price])
    """returnlist = [['Manaphy','D',
                   'https://content.tcgcollector.com/content/images/b6/bc/e2/b6bce232b85a26fd67ef2be7e0d07a40790ebe5ccb047ab41a8d6102689211f3.jpg'],
                  ['Noivern','D',
                   'https://content.tcgcollector.com/content/images/b8/d1/3b/b8d13bc33436898e384b505fbade923c7604701fac5335900d876ad7cdb78090.jpg']]"""
    return HttpResponse(json.dumps(returnlist))


def modifycard(request):
    price = request.POST.get('price')
    status = request.POST.get('status')
    cardID = request.POST.get('cardID')
    cursor = connection.cursor()
    if status == 'selling':
        cursor.execute("update OwnedCard set status = %s, c_price = %s where cardID = %s", ['selling', price, cardID])
    else:
        cursor.execute("update OwnedCard set status = %s, c_price = %s where cardID = %s", ['owned', 0, cardID])

    return redirect('/mypokemon/')


def resalepage(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        cursor.execute("select * from OwnedCard natural join Card where status='selling'")
        resalecard = cursor.fetchall()
        return render(request, 'resalepage.html', {'resalecardlist': resalecard})
    else:
        return redirect('/login/')


def buyonecard(request):
    cardID = request.POST.get('cardID')
    buyer = request.session.get('userID', None)

    if buyer == 20:
        return redirect('/resalepage/')
    today = datetime.date.today()
    paydate = today.strftime('%Y%m%d')

    cursor = connection.cursor()
    cursor.execute("select * from OwnedCard where cardID =%s", cardID)
    card = cursor.fetchone()
    cursor.execute(
        "Insert into ResaleOrder (sellerID,buyerID,cardID,trade_amount,trade_datetime) values(%s,%s,%s,%s,%s)",
        [card[2], buyer, cardID, card[4], paydate])
    cursor.execute("update OwnedCard set status = %s, c_price = %s, userID = %s where cardID = %s",
                   ['owned', 0, buyer, cardID])
    return HttpResponse(json.dumps(cardID))


def resalehistory(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        userID = request.session.get('userID', None)
        cursor.execute(
            "select r_orderID, c_name, rarity, b.u_name, y.u_name, trade_amount, trade_datetime from (select r_orderID, c_name, rarity, u_name, buyerID, trade_amount, trade_datetime from (select r_orderID, c_name, rarity, sellerID, buyerID, trade_amount, trade_datetime from ResaleOrder natural join OwnedCard natural join Card where buyerID = %s or sellerID = %s) a left join User x on a.sellerID = x.userID) b left join User y on b.buyerID = y.userID order by r_orderID desc",
            [userID, userID]
        )
        resalehistorylist = cursor.fetchall()
        return render(request, 'resalehistory.html', {'resalehistorylist': resalehistorylist})
    else:
        return redirect('/login/')

def showpricetrend(request):
    cardID=request.POST.get('cardID')
    cursor = connection.cursor()
    cursor.execute("select trade_datetime, cast(trade_amount as char) as trade_amount from ResaleOrder where cardID in (select cardID from Card natural join OwnedCard where cardID= %s) order by r_orderID desc limit 10", cardID)
    trendresult=cursor.fetchall()
    print(trendresult)
    return HttpResponse(json.dumps(trendresult))


def deleteboxhistory(request):
    orderID = request.POST.get('orderID')
    cursor = connection.cursor()
    cursor.execute(
        " delete from BoxOrder where b_orderID  = %s",orderID)
    return redirect('/boxhistory/')


def searchbox(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword', None)
        cursor = connection.cursor()
        keyword = "%" + str(keyword) + "%"

        cursor.execute("select * from BlindBox where title like %s", keyword)
        searchedbox = cursor.fetchall()

    return render(request, 'mainpage.html', {'blindboxlist': searchedbox})


def searchresalecard(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword', None)
        cursor = connection.cursor()
        keyword = "%" + str(keyword) + "%"

        cursor.execute("select * from OwnedCard natural join Card where status='selling' and c_name like %s", keyword)
        searchedresalecard = cursor.fetchall()

        return render(request, 'resalepage.html', {'resalecardlist': searchedresalecard})
    else:
        return redirect('/login/')


def searchcard(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword', None)
        cursor = connection.cursor()
        keyword = "%" + str(keyword) + "%"
        userID = request.session.get('userID', None)
        cursor.execute("select c_name,rarity, img,type,status,cardID from Card natural join OwnedCard where userID =%s and c_name like %s",
                       [userID, keyword])
        searchedcard = cursor.fetchall()

        return render(request, 'mypokemon.html', {'cardlist': searchedcard})
    else:
        return redirect('/login/')


def pricecheck(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT cardNO, c_name, type, rarity, avg(trade_amount) avgamt, count(r_orderID) FROM ResaleOrder NATURAL JOIN OwnedCard NATURAL JOIN Card GROUP BY cardNO ORDER BY avgamt desc")
        avgpricelist = cursor.fetchall()
        return render(request, 'pricecheck.html', {'avgpricelist': avgpricelist})
    else:
        return redirect('/login/')


def checkavg(request):
    if request.session.get('is_login', None):
        type = request.POST.get('cardtype', None)
        rarity = request.POST.get('cardrarity', None)
        minprice = request.POST.get('minprice', None)
        maxprice = request.POST.get('maxprice', None)

        cursor = connection.cursor()
        if minprice == '':
            minprice = 0
        if maxprice == '':
            maxprice = 1000000000

        if type == 'Choose one type':
            if rarity == 'Choose one rarity':
                cursor.execute(
                    "SELECT cardNO, c_name, type, rarity, avg(trade_amount) avgamt, count(r_orderID) FROM ResaleOrder NATURAL JOIN OwnedCard NATURAL JOIN Card GROUP BY cardNO HAVING avgamt >= %s and avgamt <= %s ORDER BY avgamt desc",
                    [minprice, maxprice])
            else:
                cursor.execute(
                    "SELECT cardNO, c_name, type, rarity, avg(trade_amount) avgamt, count(r_orderID) FROM ResaleOrder NATURAL JOIN OwnedCard NATURAL JOIN Card WHERE rarity = %s GROUP BY cardNO HAVING avgamt >= %s and avgamt <= %s ORDER BY avgamt desc",
                    [rarity, minprice, maxprice])
        else:
            if rarity == 'Choose one rarity':
                cursor.execute(
                    "SELECT cardNO, c_name, type, rarity, avg(trade_amount) avgamt, count(r_orderID) FROM ResaleOrder NATURAL JOIN OwnedCard NATURAL JOIN Card WHERE type = %s GROUP BY cardNO HAVING avgamt >= %s and avgamt <= %s ORDER BY avgamt desc",
                    [type, minprice, maxprice])
            else:
                cursor.execute(
                    "SELECT cardNO, c_name, type, rarity, avg(trade_amount) avgamt, count(r_orderID) FROM ResaleOrder NATURAL JOIN OwnedCard NATURAL JOIN Card WHERE type = %s and rarity = %s GROUP BY cardNO HAVING avgamt >= %s and avgamt <= %s ORDER BY avgamt desc",
                    [type, rarity, minprice, maxprice])
        avgpricelist = cursor.fetchall()
        return render(request, 'pricecheck.html', {'avgpricelist': avgpricelist})
    else:
        return redirect('/login/')


def adminpage(request):
    cursor = connection.cursor()
    cursor.execute("SELECT userId, count(status) as a_num, a.box_num FROM Card natural join OwnedCard natural join (SELECT userID, sum(pay_amount) as sumpay, max(pay_amount) as maxpay, count(b_orderID) as box_num FROM BoxOrder GROUP BY userID) as a  GROUP BY userID;")
    result = cursor.fetchall()
    return render(request, 'adminpage.html', {'result': result})


def adminsearch(request):
    if request.method == "POST":
        price = request.POST.get('minprice')
        rarity = request.POST.get('cardrarity')
        cursor = connection.cursor()
        cursor.execute(
            "SELECT userId, count(status) as a_num, a.box_num FROM Card natural join OwnedCard natural join (SELECT userID, sum(pay_amount) as sumpay, max(pay_amount) as maxpay, count(b_orderID) as box_num FROM BoxOrder GROUP BY userID) as a where a.sumpay >= %s and rarity = %s GROUP BY userID;",
            [price, rarity])
        result = cursor.fetchall()
    return render(request, 'adminpage.html', {'result': result})


def checkmycard(request):
    if request.method == "POST":
        cursor = connection.cursor()
        userID = request.session.get('userID', None)
        typefilter = request.POST.get('typefilter', None)
        rarityfilter = request.POST.get('rarityfilter', None)
        rarity = request.POST.getlist('rarity', None)
        types = request.POST.getlist('type', None)
        status = request.POST.getlist('status',None)
        statusfilter = request.POST.get('statusfilter1', None)

        if rarityfilter == 'allrarity':
            rarity = ['A','B','C','D']
        if statusfilter == 'allstatus':
            status = ['owned','selling']
        if typefilter == "alltypes":
            types=["Darkness","Fire","Psychic","Colorless","Water","Lightning","Grass","Fighting","Dragon","Metal","Fairy"]
        if len(rarity) == 0:
            rarity = ['A', 'B', 'C', 'D']
        if len(status) == 0:
            status = ['owned', 'selling', 'bonus']
        if len(types) == 0:
            types = types=["Darkness","Fire","Psychic","Colorless","Water","Lightning","Grass","Fighting","Dragon","Metal","Fairy"]
        print(rarity)
        cursor.execute("select c_name,rarity, img,type,status,cardID  from OwnedCard natural join Card where status in %s and type in %s and rarity in %s and userID = %s order by cardID desc",[status,types,rarity,userID])
        boxlist = cursor.fetchall
        return render(request, 'mypokemon.html', {'cardlist': boxlist})


def checkresalecard(request):
    if request.method == "POST":
        cursor = connection.cursor()
        rarityfilter = request.POST.get('rarityfilter', None)
        types = request.POST.getlist('type', None)
        minprice = request.POST.get('minprice', None)
        maxprice = request.POST.get('maxprice', None)

        if minprice != '':
            minprice = int(minprice)
        else:
            minprice = 0
        if maxprice != '':
            maxprice = int(maxprice)
        else:
            maxprice = 99999

        if rarityfilter == 'allrarity' or len(types) == 0:
            cursor.execute(
                "select * from OwnedCard natural join Card where status='selling' and (c_price >= %s and c_price <= %s)",[minprice,maxprice]
            )
        else:
            if len(types) == 1:
                cursor.execute(
                    "select * from OwnedCard natural join Card where status='selling' and rarity = %s and (c_price >= %s and c_price <= %s)", [types[0],minprice,maxprice]
                )
            if len(types) == 2:
                cursor.execute(
                    "select * from OwnedCard natural join Card where status='selling' and (rarity = %s or rarity = %s) and (c_price >= %s and c_price <= %s)", [types[0], types[1],minprice,maxprice]
                )
            if len(types) == 3:
                cursor.execute(
                    "select * from OwnedCard natural join Card where status='selling' and (rarity = %s or rarity = %s or rarity = %s) and (c_price >= %s and c_price <= %s)", [types[0], types[1], types[2],minprice,maxprice]
                )
            if len(types) == 4:
                cursor.execute(
                    "select * from OwnedCard natural join Card where status='selling' and (rarity = %s or rarity = %s or rarity = %s or rarity = %s) and (c_price >= %s and c_price <= %s)", [types[0], types[1], types[2], types[3], minprice,maxprice]
                )
        salelist = cursor.fetchall()
        return render(request, 'resalepage.html', {'resalecardlist': salelist})

def sendcard(request):
    if request.session.get('is_login', None):


        return render(request, 'sendcard.html')



def sendbonus(request):
    if request.method == "POST":
        HP = request.POST.get('AHP', None)
        MP = request.POST.get('BHP', None)
        LP = request.POST.get('CHP', None)
        cursor = connection.cursor()
        cursor.execute("call bonus2(%s,%s,%s);", [HP, MP, LP])
        bonususer = cursor.fetchall()

    return render(request, 'sendcard.html',{'bonususer':bonususer})



def dashboard(request):
    if request.session.get('is_login', None):
        cursor = connection.cursor()
        cursor.execute(
            "select count(distinct userID) from User")
        usercount=cursor.fetchone()

        cursor.execute(
            "select count(*) from OwnedCard")
        cardcount = cursor.fetchone()

        cursor.execute(
            "select count(*) from BoxOrder")
        boxordercount = cursor.fetchone()

        cursor.execute(
            "select count(*) from ResaleOrder")
        resaleordercount = cursor.fetchone()

        cardavg=round(cardcount[0]/usercount[0],2)
        boxavg = round(boxordercount[0] / usercount[0],2)
        resaleavg = round(resaleordercount[0] / usercount[0],2)



        cursor.execute(
            "select pay_datetime, count(b_orderID) from BoxOrder group by pay_datetime order by  pay_datetime asc")
        boxordertrend = cursor.fetchall()

        cursor.execute(
            "select rarity, count(cardID) from OwnedCard natural join Card where status='selling' group by rarity order by rarity asc")
        resaledistribution = cursor.fetchall()

        cursor.execute("select trade_datetime, count(*) Total, count(case when rarity = 'A' then 1 end) A,count(case when rarity = 'B' then 1 end) B, count(case when rarity = 'C' then 1 end) C, count(case when rarity = 'D' then 1 end) D from ResaleOrder natural join OwnedCard natural join Card group by trade_datetime")
        resaleorderanalysis=cursor.fetchall()

        print(boxordertrend)
        return render(request, 'dashboard.html',{'usercount':usercount[0],'cardcount':cardcount[0],'boxordercount':boxordercount[0],'resaleordercount':resaleordercount[0],'cardavg':cardavg,'boxavg':boxavg,'resaleavg':resaleavg,'boxordertrend': json.dumps(boxordertrend),'distribution':json.dumps(resaledistribution),'resaleorder':json.dumps(resaleorderanalysis)})



