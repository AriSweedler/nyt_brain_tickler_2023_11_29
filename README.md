# NYT Brain tickler November 29, 2023
I had fun solving this with my Grandma today :)

I thought the puzzle was creative and fun, and I wanted to do more! I also
thought that this would be a fun thing to code up. So I did that, and now I can
generate as many puzzles as I want (well, my script creates 692 puzzles)

# How to use
Clone the repo, then invoke `bt.py` (it stands for "brain tickler").
```
git clone git@github.com:AriSweedler/nyt_brain_tickler_2023_11_29.git
./nyt_brain_tickler_2023_11_29/bt.py --help
```

The `--help` text explains the possible arguments

    usage: bt.py [-h] [--answer] [-p PUZZLE_NUMBER]

    Generate a brain tickler puzzle in the style of the Nov. 29th 2023 puzzle.

    options:
      -h, --help            show this help message and exit
      --answer              Print the answer to the puzzle
      -p PUZZLE_NUMBER, --puzzle_number PUZZLE_NUMBER
                            The puzzle index. Must be between 0 and 691. If this is not included
                            then a random index will be selected

## Some example puzzles

This one looks tricky :)

    ❯ ./brain_tickler_2023_11_29/bt.py --puzzle_number 100
    Puzzle #100:
    _ob___
    __dd__
    ___l_r
    _a___d

This ruins the fun, but I'll print the answer out with this one

    ❯ ./brain_tickler_2023_11_29/bt.py --puzzle_number 200 --answer
    Puzzle #200:
    answer='ince'
    ___om_ - income
    ___h_s - inches
    pr____ - prince

# Improvements
The `is_valid_puzzle` function can be modified to make this a lot more
interesting. I left some comments explaining what I would maybe do.

Because I don't sort the puzzles, any modification the puzzle filtering will
cause the numbering to get randomized. So if you wanna see which puzzles your
modifications eliminate (or allow) then you'll have to do that yourself.
