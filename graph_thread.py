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
        #self.initRespect()
        #self.initPopularity()
    
    def like(self, group):
        for group in user.membership:
            self.like[group] += user.membership.group

    def respect(self, user):
        for group in user.membership:
            self.respect[group] += user.membership.group

    def support(self, group):
        for group in user.membership:
            self.respect[group] += user.membership.group

    def dislike(self, group):
        for group in user.membership:
            self.dislike[group] += user.membership.group

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
        #self.initGroups()

    def makePost(self, content, parent):
        post = postObj(self, content, parent)
        parent.addChild(post)

    def setEmail(self, email):
        self.email = email

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
        self.window = Tk()
        self.userWindow = Toplevel(self.window)
        self.curUser = users[0]

    def addUser (self, user):
        if user not in self.users:
            self.users.append(user)

    def delUser (self, user):
        self.users.remove(user)

    def showUsers(self):
        for user in self.users:
            self.showUser(user)

    def showUser(self, user):
        userText = StringVar()

        userFrame = Frame(self.userWindow)
        userFrame.grid()

        userMsg = Message(userFrame, textvariable=userText)
        userMsg.grid()
        userText.set(user.username)



    def showPosts (self):
        self.showPost(self.topPost, self.window, 0)
        self.showUsers()
        self.window.mainloop()

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
                                command = post.like)
        likeButton.grid(row=0, column=1)
        supportButton = Button(postButtons, text="support",
                                command = post.support)
        supportButton.grid(row=0, column=2)
        respectButton = Button(postButtons, text="respect",
                                command = post.respect)
        respectButton.grid(row=0, column=3)
        dislikeButton = Button(postButtons, text="dislike",
                                command = post.dislike)
        dislikeButton.grid(row=0, column=4)
        text.set(post.content)
        for child in post.children:
            self.showPost(child, window, depth + 1)

    def setGroups(self, groups):
        self.groups = groups

    def postReply(self, post):
        post.user.makePost("temp reply", post)
        self.window.destroy()
        self.window = Tk()
        self.showPosts()

reds = group(0)
blues = group(1)

reds.setConnection(blues.ID,2)
blues.setConnection(reds.ID,2)

groups = [reds, blues]

alice = user("Alice")
bob = user("Bob")

users = [alice, bob]

thread = postObj(alice, "Alice says hello!", 0)
bob.makePost("Bob says grr!", thread)
alice.makePost("That isn't nice!", thread.children[0])

forum = board(users,groups,thread)
forum.showPosts()
