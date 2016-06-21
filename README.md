# Cats

People seem to lose cats in the tube. This is a simulation to see how easily
people can find their cats back.

Couples of owner/cat are randomly placed in tube stations of London. The
simulation evolved like a game, with a main loop. For each iteration, every
owner and cat move from a station to another according to specific rules:
- Cats are not very intelligent, on each turn they'll travel randomly to one
  of the stations connected to where they are.
  Also, cats are not in a very big hurry, once in the station, they will stay
  there the next turn and leave at the following turn (This is to avoid
  infinite race between owners and cats, which could make the simulation
  neverending)
- Owners are more intelligent, they will travel to one of the stations
  connected to where they are, but (if possible) not using a station they use
  before.

However, owners can communicate with each other (via a social network for
example). If an owner sees a cat not belonging to him, he will send a message
to the other owners telling them that the cat X has been seen at the station Y.
When receiving such a message, the owner of the spotted cat will then head to
the station to hopefully find his animal around.

Every time an owner finds their cat the amount of love released is THAT big
that TFL needs to close the station to clean the love from the walls.

When a station is closed, owners and cats can leave it using any available
route, but nobody can visit this station again.

It is possible that owners and cats can get "trapped" in a station because
there is no available route to leave the stations -- that's ok, we don't care -
that's life.

An owner having found its cat stays in game and roams around. If he/she finds
another cat, as before, he will broadcast a signal for the other owners, but
because he found his cat as has nothing to do, he will follow the cat and
broadcast its position after each move. So the owner can track its cat.

When an owner receives a message saying someone is following its cat, if the
cat is unreachable (no path), the owners answers saying so. The following owner
then stops following the cat and continues to roam around.

## Usage

This project has been coded using python 3.4+

### Installation

	pip install -r requirements.txt

### Usage

	./start-cli.py --help

### Run tests

The tests can be run with the following command:

	./run-tests.py

## Improvements

- Love janitors: When a station get closed, janitors should come to clean it,
  which would take a given amount of turns during which the station would be
  closed, but would the reopen,
- Make human having found their cats follow a cat they find to help the owner
  keeping track of it,
- API interface to make a web entry point, to connect it with sockets and have a
  web representation of the network to see the cats and humans evolve,
- The simulator might be a bit big and reworked on,
- The tests could probably be improved.

## Personal notes

Often all the humans find their cat back. But sometimes some don't and reach the
maximum number of turns. I would say it comes from the following possibilities:
- They are both in parts of the graph which are separated by a closed station
  and nobody saw the cat to warn the owner of its location, which fates them to
  roam until the end of times, sad fate...
- They could find each other but are roaming in the graph without finding each
  other and nobody else sees the cat (either nobody in this part of the graph or
  just nobody crossed its path), very bad luck...
- It would be from an unspotted bug but if I disabled the closing of the
  stations (a human finding its cat back does not closes the station), 100% of
  the cats are retrieved within the allocated time.
