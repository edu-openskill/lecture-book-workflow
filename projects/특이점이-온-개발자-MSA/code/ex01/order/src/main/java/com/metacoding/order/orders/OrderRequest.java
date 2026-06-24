package com.metacoding.order.orders;

public record OrderRequest(
    int productId,
    int quantity,
    Long price,
    String address
) {}
