package com.metacoding.order.adapter.message;

public record OrderCreatedEvent(
        int orderId,
        int userId,
        int productId,
        int quantity,
        Long price,
        String address
) {}
