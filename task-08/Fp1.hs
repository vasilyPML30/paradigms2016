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
filter' f [] = []
filter' f (x : xs) | f x == True = x : (filter' f xs)
                   | otherwise = filter' f xs

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (x : xs) = foldl' f (f z x) xs

concat' :: [a] -> [a] -> [a]
concat' [] b = b
concat' (x : xs) b = x : (concat' xs b)

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x : xs) = concat' (concat' (quickSort' (filter' (< x) xs)) (filter' (== x) (concat' [x] xs))) (quickSort' (filter' (> x) xs))
