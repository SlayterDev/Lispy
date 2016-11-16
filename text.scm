(define first car)
(define rest cdr)
(define count
	(lambda (item L)
		(if L
			(+ (equal? item (first L)) (count item (rest L)))
			0)))

(define fib
	(lambda (n)
		(if (< n 2)
			1
			(+ (fib (- n 1)) (fib (- n 2))))))
(define range
	(lambda (a b)
		(if (= a b)
			(quote ())
			(cons a (range (+ a 1) b)))))
(map fib (range 0 20))
