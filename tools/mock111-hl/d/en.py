PS=[]
D=[
(1,'Look at the picture. George is dancing with ______.',['the boy in shorts','the man with glasses','the woman in a dress','the girl with long hair'],[('en-2L',1000,125,1280,400)]),
(2,'I didn’t check the news ______ I went out, so I didn’t know my train to Taipei stopped until I got to the station.',['before','but','or','though'],[]),
(3,'My ______ is watering. I can’t wait to eat the delicious food on the plate.',['eye','mouth','nose','tooth'],[]),
(4,'Turn around and take a look, Sam. There’s a cute cat ______ you.',['above','across','along','behind'],[]),
(5,'Ben: How many people ______ over for tonight’s dinner, Amy?\nAmy: Twelve. I told you last night, honey. We need to prepare enough food.',['came','are coming','would come','is going to come'],[]),
(6,'Our teacher asked us to look at problems from different ______. This way, we might fix them more easily.',['angles','answers','blanks','services'],[]),
(7,'Housewives usually have a ______ check on everything when they do shopping. They want to get the best deals.',['cheap','careful','comfortable','convenient'],[]),
(8,'Alice: ______ do you exercise each time?\nBen: Only half an hour, but I always exercise three times a day.',['How old','How fast','How long','How often'],[]),
(9,'The poor girl lost all her family in the fire. People in the town are ______ money to help her.',['building','losing','raising','taking'],[]),
(10,'I saw a man put the box at the door, but I didn’t ______ know who he was.',['actually','finally','luckily','quietly'],[]),
(11,'I don’t think Mom will allow us to join the party if we ______ our bedroom by Friday.',['don’t clean','won’t clean','wouldn’t clean','aren’t cleaning'],[]),
]
D+=[
(12,'Ivy’s birthday is on February 29th. She can only have her birthday party every four years. Her ______ birthday is finally coming and she will be twelve years old next week.',['second','third','fourth','last'],[]),
(13,'Nancy is buying a train ticket because she will ______ Taipei tomorrow.',['get on','call out','look for','leave for'],[]),
(14,'I didn’t like this picture, so Henry gave me ______. He said I had to choose between them because there was no more.',['it','one','another','the other'],[]),
(15,'Jerry and Mia broke up for some ______. They didn’t tell us what happened. We guess it’s because of their family.',['choice','experience','item','reason'],[]),
(16,'Mrs. Wang couldn’t bear to see her grandson cry, so she ______ him eat some ice cream without telling the boy’s mother.',['let','saw','told','wanted'],[]),
(17,'Joe worked for over ten hours every day last month. It almost ______ him his life. He won’t work long hours any more.',['cost','paid','saved','spent'],[]),
(18,'I think the food in the blue pot might taste ______. Those kids liked both the dishes, but they finished all the food in the blue pot but left some in the white one.',['good','better','well','best'],[]),
(19,'Ernest is looking for a place for the party with his friends. He plans to have a big meal with them and bring his pet dog along. What words should he type in to look for the information on the Net?',['Pet care','Pet food','Pet hospital','Pet-friendly restaurant'],[]),
(20,'When reading a story, Zac saw the word “flat” and didn’t know what it meant.\n“After the exciting five-day trip, Mindy went back to her common life—work, family, work, family. She felt her life was so flat. How she missed those five days!”\nHe found several meanings of the word in a dictionary. Which one should Zac choose?',['Without air.','Without power.','Not interesting.','Not very deep, thick, or high.'],[]),
]
PS+=['Below is what Arya saw on a video website.（網頁內容見附圖）\n（website 網頁　according to 根據　local 本地人）']
W=('en-3L',195,275,1210,1090)
D+=[
(21,'According to the list “You may also like these,” which topic may Arya be interested in?',['Food.','Health.','Movies.','Sports.'],[W],len(PS)-1),
(22,'Below are pictures from the video “Uphone 11 Unboxing.” What does unbox mean according to the pictures?',['Selling things to others.','Opening boxes for other people.','Teaching others how to clean cellphones.','Showing others what a new item looks like.'],[('en-3L',325,1365,1082,1620)],len(PS)-1),
]
D+=[
(23,'Arya watched one of the videos on the website, and below is what she saw in the video. Whose video did she watch?',['Trip Trip.','Eat Around.','Jane Harper.','Mindy Chen.'],[('en-3R',335,225,1100,490),W],len(PS)-1),
]
PS+=['You Can’t Live Without Vitamin C\nHow much vitamin C can we take a day? About 60 mg a day is enough. Our body can take no more than 200 mg a day.\nWhat should we know about taking vitamin C? 1. Don’t take it before meals. 2. Have enough water.\nWhy do we need vitamin C? Keep the cold away. / Make skin whiter. / Keep tooth and lip problems away. / Heart problems won’t happen easily. / Help our body take more nutrients.\nFood with vitamin C (every 100 g): Guava 137 mg, Orange 74 mg, Strawberry 69 mg, Papaya 58 mg, Lemon 34 mg, Red pepper 137 mg, Broccoli 75 mg\n（vitamin 維他命　skin 皮膚　nutrient 營養）']
V=('en-4L',165,195,1240,1090)
D+=[
(24,'What can we learn about vitamin C from the picture?',['Only fruit has vitamin C.','It is better to take vitamin C right after you get up.','Taking more than 200 mg a day doesn’t help us more.','Take vitamin C every day, and we won’t have heart attacks.'],[V],len(PS)-1),
(25,'Why is the list of “Food with vitamin C” put in the picture?',['To tell us where to buy good food.','To show us what to eat to get vitamin C.','To let us know what the most popular fruit is.','To tell us how many kinds of fruits and vegetables to eat a day.'],[],len(PS)-1),
]
PS+=['　　As a student or an office worker, you sit at the desk for so many hours every day. After school or work, you must feel tired and have a sore back. Now, I am going to tell you how to relax your sore back by doing marjaryasana.\n　　First, start on your hands and knees in a tabletop position. Begin with your knees on the mat. Make sure your knees are below your hips. Put your hands on the mat right under your shoulders, and your arms and shoulders are in line. Look straight ahead.\n　　Second, after you get ready, breathe out the air and round your back up. At the same time face down the floor. Be sure to keep your shoulders and knees in the same place as the first position. And then breathe in and come back to the first position. Repeat ten times.\n　　It’s easy, and it is also good to do “marjaryasana” on the bed after you get up. Let’s do it and relax at home!\n（relax 放鬆　position 姿勢　mat 地毯　hip 臀部　breathe 呼吸）']
D+=[
(26,'From the reading, which picture best shows marjaryasana?',['圖(A)','圖(B)','圖(C)','圖(D)'],[('en-4R',180,880,1040,1245)],len(PS)-1),
(27,'Which is NOT true about marjaryasana from the reading?',['We can’t move our knees when doing it.','It can also help relax our shoulders and hips.','We can do it both after work and after getting up.','We don’t look down on the floor in the first position.'],[],len(PS)-1),
]
PS+=['（八格漫畫，見附圖）\n1 Nancy: Nick, look at those people. They are wearing special glasses. 【That】 makes them look strange.\n2 Nick: They are watching the sun.\n3 Nancy: The sun?\n4 Nick: Yeah, don’t you notice the sun getting darker and darker? In fact, today in Taiwan, we can see an annular solar eclipse.\n5 Nancy: Annular solar eclipse? What is that?\n6 Nick: When the moon stands between and in line with the Earth and the sun, an annular solar eclipse happens. If you see through the special glasses, the sun looks like a beautiful ring.\n7 Nancy: Wow, sounds interesting. Nick: Maybe we should join them. The chance of seeing an annular solar eclipse is slim. If we miss it, we’ll have to wait two hundred years.\n8 Both: Let’s go!']
C=('en-5L',205,185,1225,1360)
D+=[
(28,'Which is an annular solar eclipse?',['圖(A)','圖(B)','圖(C)','圖(D)'],[('en-5R',185,175,1080,740)],len(PS)-1),
(29,'What does That mean?',['Wearing a ring.','Watching the sun.','Wearing the glasses.','Standing under the sun.'],[C],len(PS)-1),
(30,'Which is true?',['Nancy and Nick are going to buy the special glasses.','It is very common to see an annular solar eclipse in Taiwan.','Nancy and Nick are going to watch an annular solar eclipse.','Nancy can see an annular solar eclipse without the special glasses.'],[],len(PS)-1),
]
PS+=['　　Happy Farm is famous for its beautiful hills with hundreds of sheep around. People come here to get close to nature. Children like here because they can touch and feed the cute sheep on the farm. Also, there are several shows at the squares for visitors to watch and have some fun. At Sun Square is our most famous Sheep Shearing Show, at Star Square is Sheep Feeding Show, and at Moon Square is Horse Riding Show. We hold each show twice a day. To get to those squares, you have to take the stairs, and you can find them along Happy Road.\n　　If you would like to take your time enjoying nature at the farm, it is a good idea to stay for the night. We recommend you watch the shows at Star and Moon Square for the first day, and then check in at the glamping area at four. Here you will stay in a big and comfortable camp, with beds and a bathroom inside, and you can have our delicious dinner and breakfast. The next day, take the stairs to watch the show at Sun Square right next to the glamping area.\n（農場地圖見附圖）\n（shear 剪切　recommend 推薦）']
D+=[
(31,'Some people like to take their time getting close to nature. What will the farm recommend to them?',['Riding a horse.','Spending the night here.','Watching all the shows in one day.','Feeding the sheep along Happy Road.'],[],len(PS)-1),
(32,'What does the camp at the glamping area look like?',['圖(A)','圖(B)','圖(C)','圖(D)'],[('en-6R',180,190,1000,635)],len(PS)-1),
(33,'After getting to Happy Farm, Mike took a walk around it to watch the sheep on the hills. Now he is at the far north of the farm, and he decides to watch Sheep Feeding Show first and then Horse Riding Show. Which way is the fastest?',['Stairs A → Stairs C → Stairs D.','Stairs B → Stairs D → Stairs E.','Stairs C → Stairs D → Stairs B.','Stairs B → Stairs D → Stairs C.'],[('en-6L',520,815,910,1215)],len(PS)-1),
]
PS+=['　　What will you do if you pick up something on the street and find it is someone else’s? Most people may say they will find the person and give the thing back or hand it in to the police, but what about money? If you happen to pick up money on the street, will you do the same?\n　　A newspaper in Canada wanted to know the answer, so they started a “test” to find out where the most honest people in Canada are. The newspaper sent reporters to drop ten wallets full of money in ten Canadian cities. There was a card with a name and a phone number in each wallet. The reporters then hid around and waited to see if there would be anyone calling to send the wallet back. In the end, the reporters found 60% of the people would give the money back after they picked up the wallet. But the others would take away the money in the wallet.\n　　The reporters also found that women were more likely to give back the money. But most young people, men or women, kept the money and did not care to make the phone call. Among the ten cities, people from Moncton had a clear conscience. Toronto and Vancouver were the two cities with the lowest percentage(%) of people giving back the money. It turned out that, from the newspaper’s test, the answer was Moncton, the small town in the far west of Canada.\n（likely 可能　among 在…之中）']
D+=[
(34,'What is this reading about?',['Asking people to be honest.','Showing the findings of a study.','Talking about some cities in Canada.','Inviting people to join a newspaper’s test.'],[],len(PS)-1),
(35,'What may people with a clear conscience do?',['They may be less likely to tell lies.','They may be more likely to join studies and tests.','They may like to give foreigners a hand if they need help.','They may be more likely to pick up someone else’s things on the street.'],[],len(PS)-1),
]
D+=[
(36,'After the reporters from the newspaper finished the test, they made four pictures. Which is NOT one of them?',['圖(A)','圖(B)','圖(C)','圖(D)'],[('en-7R',175,235,580,1520)],len(PS)-1),
]
PS+=['　　Did you ever see a walking popcorn? In Andreas Kay’s video, you can see one walking on its fingers! In fact, it is a baby Flatid Planthopper Nymph insect. It looks like a small cloud or a piece of popcorn resting on little insect legs. There is a reason for this strange look—the insect is covered with white wax to keep itself safe. The insects live in Amazon rainforest, but it’s not easy to see them because they are very small (about 1 cm), and they can jump far and fast between plants (but they walk slowly). They feed on plant juice, but they don’t hurt plants. They are really interesting, aren’t they?\n---------\n　　There are many kinds of special animals in the Amazon rainforest, and the glass frog (Hyalinobatrachium fleischmanni) is one of them. Why does it get the name? Because its abdomen skin is transparent, just like glass! You can clearly see its body parts, like the stomach and the heart, through its skin. More than that, its eggs are transparent, too! Glass frogs are about 2－3 cm long, so it’s hard for us to notice them. Besides, they are really good at climbing. Come to the Taipei Zoo, and you can see the cute little frog in person!\n（wax 蠟　rainforest 雨林　abdomen skin 腹部皮膚）']
D+=[
(37,'If something is transparent, what does it mean?',['It walks slowly.','It is good at climbing.','It can jump far and fast.','People can see almost everything inside it.'],[('en-8L',595,1175,855,1500)],len(PS)-1),
]
D+=[
(38,'Sean is at the zoo with his parents, and he wants to see both glass frogs and popcorn insects. Which area of the zoo should he visit?',['(A) Sea Area','(B) Rainforest Area','(C) Night Animals','(D) Large Land Animals'],[('en-8R',325,222,1090,635)],len(PS)-1),
(39,'Sean took notes on the information above. What can he write at the bottom of the column?（column 欄）',['Its size','Its eggs','What it feeds on','How fast it can jump'],[('en-8R',412,785,998,1012)],len(PS)-1),
]
PS+=['NNC NEWS　2021/10/28\n　　Two years ago, a moose appeared on the screen of the camera in a national park in Colorado, the USA. People in the national park noticed it because __40__. Before they could do anything about it, the moose went away. Once in a while the moose would appear on the screen, and they found it was a tire.\n　　Luckily, a team found the moose, and they tried to take off the tire from it. However, its body and antlers were so big, and it was not possible to take the tire off through its head or body. So, __41__. But they found there was a steel ring inside the tire, and it was hard to cut it off. Then they chose to cut off its antlers, and the moose was finally free from the tire.\n　　You might be thinking that it was not a good idea to cut off the antlers. __42__ In early spring, antlers of moose will fall off and they will grow new ones back. Male moose count on beautiful antlers to find lovers. Though this moose with a tire could still eat and drink, __43__. After a long winter, it can finally enjoy love, just like other moose now.\n（moose 駝鹿　tire 輪胎　antler 鹿角　steel 鋼　male 雄性的）']
D+=[
(40,'空格 40 應填入：',['it looked like a giant horse','it had something around its neck','it ate lots of grass in the national park','it fought with other moose all the time'],[],len(PS)-1),
(41,'空格 41 應填入：',['they decided to cut off the tire','they gave up taking off the tire','they turned to save another moose','they gave the moose some medicine'],[],len(PS)-1),
(42,'空格 42 應填入：',['Good job.','Of course.','No worries.','You can say that again.'],[],len(PS)-1),
(43,'空格 43 應填入：',['it couldn’t find its way home','it couldn’t sleep well every night','it couldn’t find lovers with the tire','it couldn’t run as fast as other moose'],[],len(PS)-1),
]
