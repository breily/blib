import Data.Char

getlastchar :: String -> Char
getlastchar "" = chr 0
getlastchar s = s!!(length s - 1)

removelastchar :: String -> String
removelastchar "" = ""
removelastchar s = take (length s - 1) s

{-
rshash :: String -> Int -> Int
rshash s 0 = rshash s (378551 * (63889 ^ length s))
rshash "" _ = 0
rshash key a = (rshash (removelastchar key) (round (a / 63689))) * a + (ord $ getlastchar key)
-}

rshash2 :: String -> Int -> Int
rshash2 "" _ = 0
rshash2 key a = (rshash2 ((take (length key) . drop 1) key) (a * 63689)) * a + (ord $ key!!0)

{-
rshash :: String -> Int -> Int
rshash "" _ = 0
rshash (k:key) a =
    let b = a * 63689
    in (rshash key b) * a + ord k
-}

{-
rshash :: String -> Int -> Int
rshash "" _ = 0
rshash key a = 
    let b = a * 378551
    in (rshash (init key) b) * a + ord (last key)

rshash_pub :: String -> Int
rshash_pub key = rshash key 63689
-}

rshash :: String -> Int -> Int
rshash "" _ = 0
rshash key i =
    let x = 378551 * (63689 ^ i)
    --in (rshash (init key) (i + 1)) * x + ord (last key)
    in (rshash (tail key) (i - 1)) * x + ord (head key)
    
rshash_pub :: String -> Int
rshash_pub key = rshash key (length key) --0
