head' :: [a] -> a
head' (x : xs) = x

tail' :: [a] -> [a]
tail' (x : xs) = xs
tail' [] = []

take' :: Int -> [a] -> [a]
take' n [] = []
take' 0 l = []
take' n (x : xs) = [x] ++ take' (n - 1) xs

drop' :: Int -> [a] -> [a]
drop' n [] = []
drop' 0 l = l
drop' n (x : xs) = drop' (n - 1) xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' f xs = [x | x <- xs, f x == True]

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (x : xs) = foldl' f (f z x) xs

concat' :: [a] -> [a] -> [a]
concat' a b = a ++ b

filter'' :: (a -> a -> Bool) -> a -> [a] -> [a]
filter'' f a xs = [x | x <- xs, f x a == True]

less' :: Ord a => a -> a -> Bool
less' a b = a < b

more' :: Ord a => a -> a -> Bool
more' a b = a > b

eq' :: Ord a => a -> a -> Bool
eq' a b = a == b

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x : xs) = (quickSort' (filter'' less' x xs) ++ filter'' eq' x ([x] ++ xs)) ++ quickSort' (filter'' more' x xs)
