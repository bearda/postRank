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
        self.content = text
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
        self.initGroups()

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
        self.setConnection(self.ID, 1) 

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

    def addUser (self, user):
        if user not in self.users:
            self.users.append(user)

    def delUser (self, user):
        self.users.remove(user)

    def showPosts (self):
        self.showPost(self.topPost, 0)

    def showPost (self, post, depth):
        indent = "|--" * depth
        print indent + post.content
        for child in post.children:
            self.showPost(child, depth + 1)

    def setGroups(self, groups):
        self.groups = groups
