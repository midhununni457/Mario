level_1_map = [
    '                              ',
    '    c          c        2s    ',
    '   GHI         AC        AC   ',
    '          3 s                g',
    '4P       ABBC       s1      s ',
    'AC      AKFFE      ABBC     AC',
    'DE  s sAKFFFE      DFFE     DE',
    'DJMBBBLKFFFNU   2s DFFEc    DE',
    'DFFFFFFFFFFE     ABKFFSBT   DE',
    'DFFFFFFFFFFEc    DFFFFE    kDE',
    'DFFFFFFFFFFJBC   DFFFFE    AKE']
level_2_map = [
    '                              ',
    '                              ',
    '                              ',
    '                              ',
    ' P                        c   ',
    'AC                        O   ',
    'DE    s s O          s    Q  g',
    'DE   ABBBBR        WXBBBC Q s ',
    'DE   DFFFFE  c  s   DFFFEcVMBC',
    'DE   DFFFFE  O  O  kDFFFJBKFFE',
    'DE   DFFFFE  Q  Q  AKFFFFFFFFE']
level_3_map = [
    '                              ',
    '                              ',
    '                              ',
    '                              ',
    '                             g',
    '   s                          ',
    '   O          c    s    c   AC',
    ' P Q s es O   O    O    O   DE',
    'ABLYMBBBBLR   k             DE',
    'DFFFFFFFFFE   O e  c    O   DE',
    'DFFFFFFFFFE   VMBBBBBBBLR   DE']
level_4_map = [
    '                              ',
    '                              ',
    '                              ',
    '                              ',
    '                              ',
    ' P                            ',
    'AC    O         O      O     g',
    'DE s  Q  s  O   Q ce c Q      ',
    'DJMBC VMBBBLYc AYMBBBBLRc ABBC',
    'DFFFE    ce          k   eDFFE',
    'DFFFJMBBBBBBBBBBBBBBBBBBBLKFFE']
level_5_map = [
    '                                               ',
    '                                               ',
    '                                c    O         ',
    '                                AC      c      ',
    '                                        AC    g',
    '                            GHI      s         ',
    ' P               O   c eO            O      ABC',
    'AC   O  es  O   AYMBBBBLYC      s       c      ',
    'DJMC VMBBBBLR    c              AC      AC     ',
    'DFFE e   s    O  Oe  c  k   eO       O         ',
    'DFFJMBBBBBBBBLR  VMBBBBBBBBBLR                 ']

level_1 = {'node_position' : (130, 350), 'content' : level_1_map, 'unlock' : 2}
level_2 = {'node_position' : (390, 175), 'content' : level_2_map, 'unlock' : 3}
level_3 = {'node_position' : (620, 500), 'content' : level_3_map, 'unlock' : 4}
level_4 = {'node_position' : (810, 175), 'content' : level_4_map, 'unlock' : 5}
level_5 = {'node_position' : (1050, 350), 'content' : level_5_map, 'unlock' : 5}

levels = {
    1 : level_1,
    2 : level_2,
    3 : level_3,
    4 : level_4,
    5 : level_5
}