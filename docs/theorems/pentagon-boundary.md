# Pentagon boundary and finite oracle

## N2-T04 — the associator boundary closes

In any algebra over a commutative ring, define
[
[x,y,z]=x(yz)-(xy)z.
]
Then
[
[a,b,c]d+[a,bc,d]+a[b,c,d]-[a,b,cd]-[ab,c,d]=0.
]

**Proof.** Expand the five terms:
[
egin{aligned}
[a,b,c]d &= (a(bc))d-((ab)c)d,\
[a,bc,d] &= a((bc)d)-(a(bc))d,\
a[b,c,d] &= a(b(cd))-a((bc)d),\
-[a,b,cd] &= -a(b(cd))+(ab)(cd),\
-[ab,c,d] &= -(ab)(cd)+((ab)c)d.
end{aligned}
]
Every parenthesized four-letter word occurs once with each sign. ∎

The five terms are precisely the signed edge differences around the five
binary parenthesizations of (abcd). Thus the additive boundary always
closes, even when individual edges are nonzero. Non-associativity is retained
as edge data rather than erased.

## Oracle boundary

The Python experiment instantiates the scalar Cayley–Dickson construction
over (mathbb F_p) and exhausts basis quadruples. The Lean oracle does not
trust that implementation: it accepts an explicit multiplication tensor over
(mathbb Z/pmathbb Z), recomputes all products and associators, and checks
the pentagon boundary independently.

This is an executable oracle, not yet a formal proof that an input tensor is
an octonion algebra or that (p) is prime. Those are separate certificate
obligations. N2-T04 itself is proved above for every algebra, so the oracle is
a regression and evidence-replay layer.
