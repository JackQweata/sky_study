import stripe

from config.settings import PAY_PRIVATE_TOKEN


def get_payment_url(product_sky):
    stripe.api_key = PAY_PRIVATE_TOKEN

    product = stripe.Product.create(name=product_sky.title)

    price_product = stripe.Price.create(
        unit_amount=product_sky.price,
        currency="eur",
        recurring={"interval": "month"},
        product=product.id,
    )

    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price_product.id,
                "quantity": 2,
            },
        ],
        mode="subscription",
    )

    return session
