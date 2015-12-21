# [Traveler's Guide:](http://52.32.187.181:8080/)

### Introduction:
- Why: We want accurate information about our destination.
- What: Up-to-date information posted by people at correct place. Information that can be viewed by any visitor of our site.
- Construction: Django + Amazon ec2 + MemcachedCached

### Features/Challenges:
1. View, Post, Delete, Edit:
  - Visitors can view all posts.
  - Registered users can view all posts; post new post; delete, and edit their own posts.

2. GeoIP: 
  - Users can only post information about the city that they are currently in.
  - Our site automatically adds new cities that does not exist in our database.

3. City DB: 
  - Not to fan in all the time.
  - Gets city ID for sharding.
