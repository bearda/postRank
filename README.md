# postRank

Next, I have to make it so that I can add likes for a particular group.
Which means that users have to have groups. just one group for now.

so lambda: self.likePost(post)

def likePost(self, post):
    post.like(self.curUser)
