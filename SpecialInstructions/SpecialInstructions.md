# Special Instructions writeup

## 問題

Special Device Fileとほぼ同じ。添付されているファイルも同じものと思われる。

## 解き方

1. fileコマンドでファイルを確認

```
yusuke@ubuntu-ctf:~$ file runme_f3abe874e1d795ffb6a3eed7898ddcbcd929b7be 
runme_f3abe874e1d795ffb6a3eed7898ddcbcd929b7be: cannot open `runme_f3abe874e1d795ffb6a3eed7898ddcbcd929b7be' (No such file or directory)
```

-> いまいちよく分からない。

(早くも挫折)

* 参考にしたwriteup
http://moxielogic.org/blog/pages/architecture.html
[SECCON 2018 Online CTF Writeup](http://ywkw1717.hatenablog.com/entry/2018/10/28/185936)

2. readelfで確認。moxieであることが分かる。

[Architecture](http://moxielogic.org/blog/pages/architecture.htm)l

3. runmeと一緒に配られているcross-gcc494-v1.0.zipはrunmeをmoxieに対して扱えるGDBが入っているっぽい。

4. 一旦は上記のwriteupと同じGitHubのレポジトリの環境で`moxie-none-moxiebox-gdb`を実行する。

5. これで全てのアセンブラを取得。(以下は関係のある部分のみ)

```
moxie-none-moxiebox-objdump -D runme_f3abe874e1d795ffb6a3eed7898ddcbcd929b7be -m moxie
```
->
```
runme_f3abe874e1d795ffb6a3eed7898ddcbcd929b7be:     file format elf32-big


Disassembly of section .text:

0000154a <set_random_seed>:
    154a:	16 20       	bad
    154c:	04 00       	ret

0000154e <get_random_value>:
    154e:	17 20       	bad
    1550:	04 00       	ret


00001552 <decode>:
    1552:	06 18       	push	$sp, $r6
    1554:	06 19       	push	$sp, $r7
    1556:	06 1a       	push	$sp, $r8
    1558:	06 1b       	push	$sp, $r9
    155a:	06 1c       	push	$sp, $r10
    155c:	06 1d       	push	$sp, $r11
    155e:	91 18       	dec	$sp, 0x18
    1560:	02 d2       	mov	$r11, $r0                   ;flag -> $r11
    1562:	1c 42       	ld.b	$r2, ($r0)
    1564:	2e 22       	xor	$r0, $r0                    ;$r0を0にセット
    1566:	0e 42       	cmp	$r2, $r0                    
    1568:	c0 12       	beq	158e <decode+0x3c>          ;$2 == $r0(0)なら158eへ移動
    156a:	02 a3       	mov	$r8, $r1                    ;randval -> $r8
    156c:	02 9d       	mov	$r7, $r11                   ;flag -> $r7
    156e:	01 c0 00 00 	ldi.l	$r10, 0x154e
    1572:	15 4e 
    1574:	1c 8a       	ld.b	$r6, ($r8)              ;randvalの値?を1バイト -> $r6
    1576:	2e 22       	xor	$r0, $r0                    ;$r0を0にセット
    1578:	19 c0       	jsr	$r10                        ;<get_random_value>へジャンプ
    157a:	2e 82       	xor	$r6, $r0                    ;$0と$r6(randval)でxorを取っているが、この$r0には本来なら実装されたget_random_valueの戻り値が入っているのか？
    157c:	1c 29       	ld.b	$r0, ($r7)              ;flagの値? -> $r0 
    157e:	2e 82       	xor	$r6, $r0                    ;randval xor flag
    1580:	1e 98       	st.b	($r7), $r6              ;$r6を$r7へ1バイト読み込み
    1582:	89 01       	inc	$r7, 0x1                    ;$r7++
    1584:	8a 01       	inc	$r8, 0x1                    ;$r8++
    1586:	1c 39       	ld.b	$r1, ($r7)              ;$r7の1バイトを$r1へロード
    1588:	2e 22       	xor	$r0, $r0                    ;$r = 0
    158a:	0e 32       	cmp	$r1, $r0                    
    158c:	c7 f3       	bne	1574 <decode+0x22>          ;$r1 != $r0ならば、1574へジャンプ
    158e:	02 2d       	mov	$r0, $r11                   ;$11に残っているflag -> $r0
    1590:	02 e0       	mov	$r12, $fp                   ;$fpはフレームポインタ。リターンアドレスとかが入ってる?
    1592:	9e 18       	dec	$r12, 0x18
    1594:	07 ed       	pop	$r12, $r11
    1596:	07 ec       	pop	$r12, $r10
    1598:	07 eb       	pop	$r12, $r9
    159a:	07 ea       	pop	$r12, $r8
    159c:	07 e9       	pop	$r12, $r7
    159e:	07 e8       	pop	$r12, $r6
    15a0:	04 00       	ret

000015a2 <main>:
    15a2:	06 18       	push	$sp, $r6
    15a4:	91 18       	dec	$sp, 0x18
    15a6:	01 20 92 d6 	ldi.l	$r0, 0x92d68ca2
    15aa:	8c a2 
    15ac:	03 00 00 00 	jsra	154a <set_random_seed>
    15b0:	15 4a 
    15b2:	01 80 00 00 	ldi.l	$r6, 0x1480
    15b6:	14 80 
    15b8:	01 20 00 00 	ldi.l	$r0, 0x1
    15bc:	00 01 
    15be:	01 30 00 00 	ldi.l	$r1, 0x1654
    15c2:	16 54 
    15c4:	19 80       	jsr	$r6
    15c6:	01 20 00 00 	ldi.l	$r0, 0x1
    15ca:	00 01 
    15cc:	01 30 00 00 	ldi.l	$r1, 0x1680
    15d0:	16 80 
    15d2:	19 80       	jsr	$r6
    15d4:	01 20 00 00 	ldi.l	$r0, 0x1
    15d8:	00 01 
    15da:	01 30 00 00 	ldi.l	$r1, 0x169c
    15de:	16 9c 
    15e0:	19 80       	jsr	$r6
    15e2:	01 20 00 00 	ldi.l	$r0, 0x1
    15e6:	00 01 
    15e8:	01 30 00 00 	ldi.l	$r1, 0x16ac
    15ec:	16 ac 
    15ee:	19 80       	jsr	$r6
    15f0:	01 20 00 00 	ldi.l	$r0, 0x1
    15f4:	00 01 
    15f6:	01 30 00 00 	ldi.l	$r1, 0x16c4
    15fa:	16 c4 
    15fc:	19 80       	jsr	$r6
    15fe:	01 20 00 00 	ldi.l	$r0, 0x1
    1602:	00 01 
    1604:	01 30 00 00 	ldi.l	$r1, 0x16e0
    1608:	16 e0 
    160a:	19 80       	jsr	$r6
    160c:	01 20 00 00 	ldi.l	$r0, 0x1800                 ;flag
    1610:	18 00 
    1612:	01 30 00 00 	ldi.l	$r1, 0x1820                 ;randval
    1616:	18 20 
    1618:	03 00 00 00 	jsra	1552 <decode>
    161c:	15 52 
    161e:	02 32       	mov	$r1, $r0
    1620:	01 20 00 00 	ldi.l	$r0, 0x1
    1624:	00 01 
    1626:	19 80       	jsr	$r6
    1628:	01 20 00 00 	ldi.l	$r0, 0x1
    162c:	00 01 
    162e:	01 30 00 00 	ldi.l	$r1, 0x167c
    1632:	16 7c 
    1634:	19 80       	jsr	$r6
    1636:	2e 22       	xor	$r0, $r0
    1638:	03 00 00 00 	jsra	144a <exit>
    163c:	14 4a 

Disassembly of section .data:

00001800 <flag>:
    1800:	6d 72       	bad
    1802:	c3 e2       	beq	17c8 <_erodata+0xd8>
    1804:	cf 95       	bgt	1730 <_erodata+0x40>
    1806:	54 9d       	bad
    1808:	b6 ac       	ssr	$r4, 0xac
    180a:	03 84 c3 c2 	jsra	c3c23593 <_end+0xc3c21933>
    180e:	35 93 
    1810:	c3 d7       	beq	17c0 <_erodata+0xd0>
    1812:	7c e2       	bad
    1814:	dd d4       	ble	1bbe <_ebss+0x35e>
    1816:	ac 5e       	gsr	$r10, 0x5e
    1818:	99 c9       	dec	$r7, 0xc9
    181a:	a5 34       	gsr	$r3, 0x34
    181c:	de 06       	ble	142a <__write+0x2>
    181e:	4e 00       	bad

00001820 <randval>:
    1820:	3d 05       	bad
    1822:	dc 31       	ble	1886 <_ebss+0x26>
    1824:	d1 8a       	bltu	1b3a <_ebss+0x2da>
    1826:	af 29       	gsr	$r13, 0x29
    1828:	96 fa       	dec	$r4, 0xfa
    182a:	cb 1b       	blt	1662 <_etext+0x24>
    182c:	01 ec e2 f7 	ldi.l	$r12, 0xe2f71570
    1830:	15 70 
    1832:	6c f4       	bad
    1834:	7e a1       	bad
    1836:	9e 0e       	dec	$r12, 0xe
    1838:	01 f9 c2 4c 	ldi.l	$r13, 0xc24cbaa0
    183c:	ba a0 
    183e:	a1 08       	gsr	$sp, 0x8
    1840:	70 24       	bad
    1842:	85 8a       	inc	$r3, 0x8a
    1844:	4d 2d       	bad
    1846:	3c 02       	bad
    1848:	fc 6f       	bad
    184a:	20 f0 c7 ad 	ldi.s	$r13, 0xc7ad2f97
    184e:	2f 97 
    1850:	2b cc       	or	$r10, $r10
    1852:	a3 34       	gsr	$r1, 0x34
    1854:	23 53       	st.s	($r3), $r1
    1856:	c9 b7       	blt	1bc6 <_ebss+0x366>
    1858:	0c 10 6c 0e 	ldo.l	$sp, 0x6c0e($fp)
    185c:	fa f9       	bad
    185e:	a1 9a       	gsr	$sp, 0x9a

```


`set_random_seed`を呼び出していて、その前でr0に`0x92d68ca2`を引数として渡そうとしているらしいことが分かる。そして、この`0x92d68ca2`で検索をかけるとxorshift関連のページが先頭に出てくるので、ここからxorshiftを使用すると考えられそう。`0x92d68ca2`は10進数だと`2463534242`で、xorshiftのwikipediaでもseedとして使用されているのでseedとして使うと分かる。

* 他にもstringsを使うと`moxie`や`xorshift`という文字列を確認できる。上記のアセンブラで未実装のメソッドについても教えてくれている。

```

yusuke@ubuntu-ctf:~/Downloads/moxiebox$ strings ../../Documents/SpecialInstructions/runme_f3abe874e1d795ffb6a3eed7898ddcbcd929b7be
,.U7
0123456789abcdef
This program uses special instructions.
SETRSEED: (Opcode:0x16)
	RegA -> SEED
GETRAND: (Opcode:0x17)
	xorshift32(SEED) -> SEED
	SEED -> RegA
GCC: (GNU) 4.9.4
moxie-elf.c
decode
putchar
```

6. アセンブラを読む限り、`set_random_seed`と`get_random_value`は実装されていない様子。この関数の部分に絞って実装する方法もあるようだが、(多くのwriteupに従って)pythonで対応するコードを作成する方向で進める。

* xorshift32で使用する3値は[wikipedia](https://ja.wikipedia.org/wiki/Xorshift)を参考に13,15,17を使用する。ここはなんとなくでこの数字を使用している人が多いようだが、以下のwriteupではソルバを使用してこの3値を決定していた。

[SECCON 2018 Online CTF Writeup](https://hikalium.hatenablog.jp/entry/2018/10/28/164812)

7. 上記のコードをpythonで書き換えると以下のようになる。以下のサイトのコピペです。

[Special Instructions](https://github.com/PDKT-Team/ctf/tree/master/seccon2018/special-instructions)


``` py
import numpy as np

state = np.uint32(0x92d68ca2)
def xorshift():
    global state
    state ^= np.uint32(state << 13);
    state ^= np.uint32(state >> 17);
    state ^= np.uint32(state << 15);
    return np.uint32(state);

flag = "6d72c3e2cf95549db6ac0384c3c23593c3d77ce2ddd4ac5e99c9a534de064e00".decode("hex")
r = "3d05dc31d18aaf2996facb1b01ece2f715706cf47ea19e0e01f9c24cbaa0a108".decode("hex")

s = ""
for i, c in enumerate(flag):
    if c == "\x00":
        break
    xorshift()問題
    s += chr((ord(c) ^ ord(r[i]) ^ state) & 0xff)
print s
```
->
```
% python sample.py
SECCON{MakeSpecialInstructions}
```

#### その他Writeup

* [SECCON 2018 参戦記](https://garasubo.github.io/hexo/2018/10/31/seccon.html)
* [SECCON 2018 Online CTF Writeup](https://hikalium.hatenablog.jp/entry/2018/10/28/164812)
* [SECCON 2018 Online CTF writeup](https://hiziriai.hatenablog.com/entry/2018/10/28/203322)
* [Special Instructions](https://ctftime.org/task/6937)
    * 他の問題のwriteupもまとまっているっぽい。[Tasks](https://ctftime.org/event/683/tasks/)