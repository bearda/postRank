from Tkinter import *
from snap import *
#postObj
#
# members:
#   user        This is the user who posted this
#   content     this is the string containing the text/html for the post
#   parent      this is the postObj that this postObj is in reply to
#   scores:
#       likes   list of users who liked this
#       respects
#       support
#       dislike
#   ID          This is the post ID, for accounting purposes
#   children    This is the list of child postObj

class postObj:


    def __init__ (self, user, content, parent):
        self.user = user
        self.content = content
        self.parent = parent
        self.ID = 0 #TODO global incrementing variable
        self.children = []

        #TODO: initialize dicto with all zero members
        self.initScores()
        self.score = 0 #this is a dummy int used by sorting methods
    
    def initScores(self):
        self.groups = []
        self.likes = {}
        self.likeList = []
        self.respects = {}
        self.respectList = []
        self.supports = {}
        self.supportList = []
        self.dislikes = {}
        self.dislikeList = []
        for group in self.user.membership:
            self.groups.append(group)
            self.likes[group] = 0
            self.respects[group] = 0
            self.supports[group] = 0
            self.dislikes[group] = 0

    def like(self, user):
        for group in user.membership:
            if group not in self.groups:
                self.likes[group] = 0
            self.likes[group] += user.membership[group]

    def respect(self, user):
        for group in user.membership:
            if group not in self.groups:
                self.respects[group] = 0
            self.respects[group] += user.membership[group]

    def support(self, user):
        for group in user.membership:
            if group not in self.groups:
                self.supports[group] = 0
            self.supports[group] += user.membership[group]

    def dislike(self, user):
        for group in user.membership:
            if group not in self.groups:
                self.dislikes[group] = 0
            self.dislikes[group] += user.membership[group]

    def countLikes(self):
        return sum(x[1] for x in self.likes.items())
    def countRespects(self):
        return sum(x[1] for x in self.respects.items())
    def countSupports(self):
        return sum(x[1] for x in self.supports.items())
    def countDislikes(self):
        return sum(x[1] for x in self.dislikes.items())

    def addChild(self, child):
        self.children.append(child)

    def delChild(self, child):
        #TODO: adjust ranking
        self.children.remove(child)

#A user. they make posts
#
#members:
#   username        A string, identifying the user
#   email           An email address associated with the user
#   ID              A unique ID for this user
#   membership      A dict with the membership score for each group

class user:


    def __init__(self, username, ID):
        self.username = username
        self.email = "" #no email by default
        self.ID = ID
        self.initGroups()

    def makePost(self, content, parent):
        post = postObj(self, content, parent)
        parent.addChild(post)

    def setEmail(self, email):
        self.email = email

    def initGroups(self):
        self.membership = {}

    def setGroups(self, groups):
        self.membership = groups

#A group. This is a list of users, and a dict of connection strengths
#to all other groups.
# members:
#   ID          Globally unique ID
#   users       A list of users
#   connections A dict of connection strengths to other groups.
#                 Essentially, this is how valueable a link to the 
#                 other group is


class group:

    def __init__ (self, groupID):
        self.ID = groupID
        self.users = []
        self.initConnections()
        self.setConnection(self.ID, 1) 

    def initConnections(self):
        self.connections = {}

    def setConnection(self, connectionID, strength):
        self.connections[connectionID] = strength

    def getConnection(self, connectionID):
        if (connectionID in self.connections):
            return self.connections[connectionID]
        return 0

#this has children, users, groups, and methods for displaying them
class board:

    def __init__ (self, users, groups, post):
        self.users = users
        self.groups = groups
        self.topPost = post
        self.curUser = users[0]
        self.curID = self.topPost.ID + 1

    def addUser (self, user):
        if user not in self.users:
            self.users.append(user)

    def delUser (self, user):
        self.users.remove(user)

    def changeCurUser(self, user):
        self.curUser = user
        self.curUserText.set(self.curUser.username)

    def startWindows(self):
        self.window = Tk()
        self.userWindow = Toplevel(self.window)
        self.rankWindow = Toplevel(self.window)
        self.mainFrame = Frame(self.window)
        self.mainFrame.grid()
        self.showPosts()
        self.showUsers()
        self.showRankWindow()
        self.window.mainloop()

    def showUsers(self):
        #show current user
        curUserFrame = Frame(self.userWindow)
        curUserFrame.grid()
        self.curUserText = StringVar()
        curUserMsg = Message(curUserFrame, textvariable=self.curUserText)
        self.curUserText.set(self.curUser.username)
        curUserMsg.grid()

        #show all the users
        for user in self.users:
            self.showUser(user)

    def showUser(self, user):
        userFrame = Frame(self.userWindow)
        userFrame.grid()

        userBtn = Button(userFrame, text=user.username,
                          command = lambda: self.changeCurUser(user))
        userBtn.grid(padx=20,pady=10)

    def showRankWindow(self):
        hintText = StringVar()
        hintMsg = Message(self.rankWindow, textvariable=hintText, aspect=500)
        hintMsg.grid()
        hintText.set("Click on the desired sorting method")

        btnFrame = Frame(self.rankWindow)
        btnFrame.columnconfigure(0, weight=1)
        btnFrame.grid(sticky=E+W)
        
        byLikes = Button(btnFrame, text="likes", 
                command=self.setSortByLikes)
        byLikes.columnconfigure(0, weight=1)
        byLikes.grid(sticky=E+W)
        
        byRespects = Button(btnFrame, text="Respects", 
                command=self.setSortByRespects)
        byRespects.columnconfigure(0, weight=1)
        byRespects.grid(sticky=E+W)
        
        bySupports = Button(btnFrame, text="Supports", 
                command=self.setSortBySupports)
        bySupports.columnconfigure(0, weight=1)
        bySupports.grid(sticky=E+W)

        byHardStuff = Button(btnFrame, text="HardStuff", 
                command=self.setSortByHardStuff)
        byHardStuff.columnconfigure(0, weight=1)
        byHardStuff.grid(sticky=E+W)

    def showPosts (self):
        self.showPost(self.topPost, self.mainFrame, 0)

    def showPost (self, post, window, depth):
        print post.ID
        print post.content
        indent = 30 * depth
        text = StringVar()
        data = StringVar()

        postFrame = Frame(window)
        postFrame.grid(padx=(indent,10))

        dataMsg = Message(postFrame, textvariable=data, aspect=3000)
        data.set("Poster: %s  Likes: %d  Respects: %d  Supports: %d"
                "  Dislikes: %d" % (post.user.username, post.countLikes(),
                                    post.countRespects(), post.countSupports(),
                                    post.countDislikes()))
        dataMsg.grid(row=0,sticky="ew",columnspan=3)

        contentMsg = Message(postFrame, textvariable=text)
        contentMsg.grid(row=1, column=0)

        postButtons = Frame(postFrame)
        postButtons.grid(row=1, column=1)
        replyButton = Button(postButtons, text="reply",
                command = lambda: self.postReply(post))
        replyButton.grid(row=0, column=0)
        likeButton = Button(postButtons, text="like",
                command = lambda: self.likePost(post))
        likeButton.grid(row=0, column=1)
        supportButton = Button(postButtons, text="support",
                command = lambda: self.supportPost(post))
        supportButton.grid(row=0, column=2)
        respectButton = Button(postButtons, text="respect",
                command = lambda: self.respectPost(post))
        respectButton.grid(row=0, column=3)
        dislikeButton = Button(postButtons, text="dislike",
                command = lambda: self.dislikePost(post))
        dislikeButton.grid(row=0, column=4)
        text.set(post.content)
        for child in post.children:
            self.showPost(child, window, depth + 1)

    def setGroups(self, groups):
        self.groups = groups

    def postReply(self, post):
        self.curUser.makePost("temp reply", post)
        post.children[-1].ID = self.curID
        self.curID += 1
        self.refreshWindows()

    def postReplySetup(self, post, text, user):
        user.makePost(text, post)
        post.children[-1].ID = self.curID
        self.curID += 1

    def refreshWindows(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.window)
        self.mainFrame.grid()
        self.showPosts()

    def likePost(self, post):
        post.like(self.curUser)
        self.refreshWindows()
    def respectPost(self, post):
        post.respect(self.curUser)
        self.refreshWindows()
    def supportPost(self, post):
        post.support(self.curUser)
        self.refreshWindows()
    def dislikePost(self, post):
        post.dislike(self.curUser)
        self.refreshWindows()

    def setSortByLikes(self):
        self.sortByLikes(self.topPost)
        self.refreshWindows()
    def sortByLikes(self, post):
        post.children = sorted(post.children, reverse=True,
                key = self.sortByLikes)
        return post.countLikes()
    def setSortByRespects(self):
        self.sortByRespects(self.topPost)
        self.refreshWindows()
    def sortByRespects(self, post):
        post.children = sorted(post.children, reverse=True,
                key = self.sortByRespects)
        return post.countRespects()
    def setSortBySupports(self):
        self.sortBySupports(self.topPost)
        self.refreshWindows()
    def sortBySupports(self, post):
        post.children = sorted(post.children, reverse=True,
                key = self.sortBySupports)
        return post.countSupports()

    def setSortByHardStuff(self):
        self.sortByHardStuff(self.topPost)
        self.refreshWindows()
    def sortByHardStuff(self, post):
        post.children = sorted(post.children, reverse=True,
                key = self.sortByHardStuff)

        score = sum(child.score for child in post.children)
        score += post.countLikes()
        score += post.countRespects()
        score += post.countSupports()
        score -= post.countDislikes()

        return score

class BoardGraph():
    def __init__(self, board):
        self.hack = 15
        self.biGraph = TNGraph.New()
        self.initNodes(board)
        self.initLinks(board)
        self.graph = TUNGraph()
        #Display stuff
        print "look here!"
        print self.biGraph.GetNodes()
        print self.biGraph.GetEdges()
        DrawGViz(self.biGraph, gvlDot, "graph2.png", "graph 1")
        print "look here!"


    def initNodes(self, board):
        #user nodes
        i=0
        for user in board.users:
            self.biGraph.AddNode(user.ID)
            print user.ID
            i = max(user.ID,i)
        #post nodes
        self.addPostNode(board.topPost, i)

    def addPostNode(self, post, offset):
        for child in post.children:
            self.addPostNode(child, offset)
        print post.ID
        self.biGraph.AddNode(offset + post.ID + 1)
        self.biGraph.AddEdge(post.user.ID, offset + 1 + post.ID)

    def initLinks(self, board):
        return

reds = group(0)
blues = group(1)

reds.setConnection(blues.ID,2)
blues.setConnection(reds.ID,2)

groups = [reds, blues]
redMember = {reds:1,blues:0}
blueMember = {reds:0,blues:1}

alice = user("Alice", 1)
alice.setGroups(redMember)
bob = user("Bob", 2)
bob.setGroups(blueMember)

users = [alice, bob]

thread = postObj(alice, "Alice says hello!", 1)
forum = board(users,groups,thread)
forum.postReplySetup(thread, "Bob says grr!", bob)
forum.postReplySetup(thread.children[0], "That isn't nice!", alice)

forum.startWindows()
network = BoardGraph(forum)

