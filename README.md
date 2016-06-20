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
