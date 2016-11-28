import Prelude hiding (lookup)

data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup key Nil = Nothing
lookup key (Node k v l r) | key == k = Just v
                          | key < k = lookup key l
                          | key > k = lookup key r

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert key value Nil = (Node key value Nil Nil)
insert key value (Node k v l r) | key == k = Node key value l r 
                                | key < k = Node k v (insert key value l) r
                                | key > k = Node k v l (insert key value r)

leftmost :: BinaryTree k v -> k
leftmost (Node k v Nil r) = k
leftmost (Node k v l r) = leftmost l

get :: Maybe v -> v
get (Just b) = b

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete key Nil = Nil
delete key (Node k v Nil r) | key > k = Node k v Nil (delete key r)
                            | key == k = r
delete key (Node k v l Nil) | key < k = Node k v (delete key l) Nil
                            | key == k = l
delete key (Node k v l r) | key < k = Node k v (delete key l) r
                          | key > k = Node k v l (delete key r)
                          | key == k = Node k' (get (lookup k' r)) l (delete k' r)
                                     where k' =  leftmost r
