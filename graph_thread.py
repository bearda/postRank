from Tkinter import *
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
    
    def initScores(self):
        self.groups = []
        self.likes = {}
        self.respects = {}
        self.supports = {}
        self.dislikes = {}
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


    def __init__(self, username):
        self.username = username
        self.email = "" #no email by default
        self.ID = 0 #TODO: give unique IDs
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
        self.showPosts()
        self.showUsers()
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

    def showPosts (self):
        self.showPost(self.topPost, self.window, 0)

    def showPost (self, post, window, depth):
        indent = 30 * depth
        text = StringVar()
        postFrame = Frame(window)
        postFrame.grid(padx=(indent,10))
        windowPost = Message(postFrame, textvariable=text)
        windowPost.grid(column=0)
        postButtons = Frame(postFrame)
        postButtons.grid(row=0, column=1)
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
        post.user.makePost("temp reply", post)
        self.window.destroy()
        self.startWindows()

    def likePost(self, post):
        post.like(self.curUser)
        print post.likes
    def respectPost(self, post):
        post.respect(self.curUser)
        print post.likes
    def supportPost(self, post):
        post.support(self.curUser)
        print post.likes
    def dislikePost(self, post):
        post.dislike(self.curUser)
        print post.likes

reds = group(0)
blues = group(1)

reds.setConnection(blues.ID,2)
blues.setConnection(reds.ID,2)

groups = [reds, blues]
redMember = {reds:1,blues:0}
blueMember = {reds:0,blues:1}

alice = user("Alice")
alice.setGroups(redMember)
bob = user("Bob")
bob.setGroups(blueMember)

users = [alice, bob]

thread = postObj(alice, "Alice says hello!", 0)
bob.makePost("Bob says grr!", thread)
alice.makePost("That isn't nice!", thread.children[0])

forum = board(users,groups,thread)
forum.startWindows()
